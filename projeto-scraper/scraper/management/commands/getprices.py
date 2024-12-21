from django.core.management.base import BaseCommand
from scraper.models import URL
from scraper.services.scraper_amigao import ScraperAmigao


class Command(BaseCommand):
    help = "Fetch product data from registered URLs and save it to the database"

    def handle(self, *args, **kwargs):
        urls = URL.objects.all()
        for url_obj in urls:
            scraper = ScraperAmigao(url_obj.url, url_obj.store)
            scraper.extract_url()

        print("Todas as URLs foram extraídas com sucesso.")
