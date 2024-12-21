import requests
from bs4 import BeautifulSoup

from scraper.models import Category, History, Product


class ScraperAmigao:
    def __init__(self, url, store):
        self.url = url
        self.store = store
        self.page = None
        self.category = None

    def parse_page(self):
        if self.url is None:
            return None

        response = requests.get(self.url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "lxml")
        return None

    def next_page(self):
        next_page = self.page.find(class_="action next")

        if next_page:
            return next_page["href"]
        else:
            return None

    def extract_category(self):
        category_element = self.page.find(
            attrs={"data-ui-id": "page-title-wrapper"},
        )
        return category_element.text.strip() if category_element else None

    def determine_offer(self, product_element):
        return product_element.find(attrs={"data-price-type": "oldPrice"}) is not None

    def extract_product_name(self, product_element):
        product_name_element = product_element.find("a", class_="product-item-link")
        return product_name_element.text.strip() if product_name_element else None

    def extract_product_sku(self, product_element):
        sku_element = product_element.find(attrs={"data-product-sku": True})
        return sku_element["data-product-sku"] if sku_element else None

    def extract_offer_prices(self, product_element):
        old_price_element = product_element.find(
            attrs={"data-price-type": "oldPrice", "data-price-amount": True}
        )
        new_price_element = product_element.find(
            attrs={"data-price-type": "finalPrice", "data-price-amount": True}
        )

        old_price = (
            old_price_element["data-price-amount"] if old_price_element else None
        )
        new_price = (
            new_price_element["data-price-amount"] if new_price_element else None
        )

        return old_price, new_price

    def extract_normal_price(self, product_element):
        price_element = product_element.find(
            attrs={"data-price-type": "finalPrice", "data-price-amount": True}
        )
        return price_element["data-price-amount"] if price_element else None

    def extract_product(self, product_element):
        if not self.page:
            print(f"Erro ao carregar a URL: {self.url}")
            return None

        sku = self.extract_product_sku(product_element)
        name = self.extract_product_name(product_element)

        offer = self.determine_offer(product_element)

        if offer:
            old_price, current_price = self.extract_offer_prices(product_element)
        else:
            old_price = None
            current_price = self.extract_normal_price(product_element)

        if not name or not sku or not current_price:
            print(f"Falha ao extrair todos os detalhes da URL: {self.url}")
            return None

        product_data = {
            "name": name,
            "sku": sku,
            "current_price": float(current_price),
            "old_price": float(old_price) if old_price else None,
            "offer": offer,
        }

        message = f"Produto {product_data['name']} (SKU {product_data['sku']}) está custando {product_data['current_price']}"

        if offer:
            message = (
                f"[OFERTA] {message} (preço anterior: {product_data['old_price']})"
            )

        print(message)

        return product_data

    def extract_page(self):
        print("Extraindo página:", self.url)
        base_page = self.page.find(id="maincontent")
        if not base_page:
            print("Não foi possível encontrar onde o início da página está localizado")
            return

        page_products = base_page.find_all_next(class_="item product product-item")

        category_instance, _ = Category.objects.get_or_create(name=self.category)

        for page_product in page_products:
            product_data = self.extract_product(page_product)

            if product_data is None:
                continue

            product, created = Product.objects.get_or_create(
                sku=product_data["sku"],
                defaults={
                    "description": product_data["name"],
                    "store": self.store,
                    "category": category_instance,
                },
            )

            if not created:
                product.description = product_data["name"]
                product.category = category_instance
                product.save()

            History.objects.create(
                product=product,
                default_price=product_data["old_price"]
                or product_data["current_price"],
                offer_price=(
                    product_data["current_price"] if product_data["offer"] else None
                ),
                offer=product_data["offer"],
                category=category_instance,
            )

    def extract_url(self):
        self.page = self.parse_page()

        if not self.page:
            print(f"Erro ao carregar a URL: {self.url}. Verifique se é uma URL válida!")
            return

        self.category = self.extract_category()

        while self.url:
            self.extract_page()
            self.url = self.next_page()
            self.page = self.parse_page()
