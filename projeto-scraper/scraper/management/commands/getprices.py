from django.core.management.base import BaseCommand
from scraper.models import URL, Product, History, Category
from scraper.actions import parse_url, extract_category, extract_products_from_page, extract_pagination_links


class Command(BaseCommand):
    help = "Fetch product data from category pages and save to the database"

    def handle(self, *args, **kwargs):
        urls = URL.objects.all()
        for url_obj in urls:
            print(f"Fetching data from: {url_obj.url}")
            soup = parse_url(url_obj.url)
            if not soup:
                print(f"Failed to fetch data from URL: {url_obj.url}")
                continue

            category_name = extract_category(soup)
            category, _ = Category.objects.get_or_create(name=category_name)
            print(f"Categoria identificada: {category_name}")

            products = extract_products_from_page(soup)
            pagination_links = extract_pagination_links(soup)

            for link in pagination_links:
                print(f"Fetching data from additional page: {link}")
                page_soup = parse_url(link)
                if page_soup:
                    products.extend(extract_products_from_page(page_soup))

            if not products:
                print(f"No products found in URL: {url_obj.url}")
                continue

            for product_data in products:
                product, created = Product.objects.get_or_create(
                    sku=product_data["sku"],
                    defaults={
                        "description": product_data["name"],
                        "store": url_obj.store,
                        "category": category,
                    },
                )

                if not created:
                    product.description = product_data["name"]
                    product.category = category
                    product.save()

                History.objects.create(
                    product=product,
                    default_price=product_data["old_price"] or product_data["current_price"],
                    offer_price=product_data["current_price"] if product_data["offer"] else None,
                    offer=product_data["offer"],
                )

                print(
                    f"O produto '{product_data['name']}' com SKU {product_data['sku']} custa {product_data['current_price']:.2f}"
                    + (f" e antes custava {product_data['old_price']:.2f}" if product_data["old_price"] else "")
                )

        print("Finished processing all URLs.")
