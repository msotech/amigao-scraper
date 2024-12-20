from django.core.management.base import BaseCommand
from scraper.models import URL, Product, History
from scraper.actions import extract_product


class Command(BaseCommand):
    help = "Fetch product data from registered URLs and save it to the database"

    def handle(self, *args, **kwargs):
        urls = URL.objects.all()
        for url_obj in urls:
            print(f"Fetching data from: {url_obj.url}")
            product_data = extract_product(url_obj.url)

            if not product_data:
                print(f"Skipping URL: {url_obj.url}")
                continue

            product, created = Product.objects.get_or_create(
                sku=product_data["sku"],
                defaults={
                    "description": product_data["name"],
                    "store": url_obj.store,
                },
            )

            if not created:
                product.description = product_data["name"]
                product.save()

            History.objects.create(
                product=product,
                default_price=product_data["old_price"] or product_data["current_price"],
                offer_price=product_data["current_price"] if product_data["offer"] else None,
                offer=product_data["offer"],
            )

            if product_data["offer"]:
                print(
                    f"[Oferta] O produto '{product_data['name']}' com SKU {product_data['sku']} custa {product_data['current_price']:.2f} "
                    f"e antes custava {product_data['old_price']:.2f}"
                )
            else:
                print(
                    f"O produto '{product_data['name']}' com SKU {product_data['sku']} custa {product_data['current_price']:.2f}"
                )

        print("Finished processing all URLs.")
