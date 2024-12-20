import requests
from bs4 import BeautifulSoup


def parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None


def extract_category(soup):
    category_element = soup.find("span", attrs={"data-ui-id": "page-title-wrapper"})
    if category_element:
        return category_element.text.strip()
    return "Categoria desconhecida"


def extract_products_from_page(soup):
    products = []
    product_elements = soup.find_all("li", class_="item product product-item")

    for product_element in product_elements:
        name_element = product_element.find("a", class_="product-item-link")
        name = name_element.text.strip() if name_element else "Produto desconhecido"

        sku_element = product_element.find(attrs={"data-product-id": True})
        sku = sku_element["data-product-id"] if sku_element else None

        if not sku:
            print(f"Produto ignorado por não ter SKU: {name}")
            continue

        promo_price_element = product_element.find("span", class_="special-price")
        promo_price = None
        if promo_price_element:
            price_span = promo_price_element.find("span", class_="price")
            promo_price = float(price_span.text.strip().replace("R$", "").replace(",", ".")) if price_span else None

        original_price_element = product_element.find("span", class_="old-price")
        original_price = None
        if original_price_element:
            price_span = original_price_element.find("span", class_="price")
            original_price = float(price_span.text.strip().replace("R$", "").replace(",", ".")) if price_span else None

        if not promo_price:
            price_span = product_element.find("span", class_="price")
            promo_price = float(price_span.text.strip().replace("R$", "").replace(",", ".")) if price_span else None

        offer = original_price is not None and promo_price < original_price

        products.append({
            "name": name,
            "sku": sku,
            "current_price": promo_price,
            "old_price": original_price if offer else None,
            "offer": offer,
        })

    return products


def extract_pagination_links(soup):
    pagination_links = []
    pages = soup.find("div", class_="pages")
    if not pages:
        return pagination_links

    page_links = pages.find_all("a", href=True, class_="page")
    for page_link in page_links:
        link = page_link["href"]
        if link not in pagination_links:
            pagination_links.append(link)

    return pagination_links
