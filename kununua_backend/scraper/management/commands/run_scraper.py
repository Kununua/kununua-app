from django.core.management.base import BaseCommand
from location.models import Country, Currency
from scraper.scrapers.spain import scraper_el_jamon
from scraper.scrapers.spain import scraper_mercadona
from scraper.scrapers.spain import scraper_carrefour
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
import pandas as pd
import time

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        API = ScraperSQLiteAPI()
        
        start = time.time()
        scraper_carrefour.scraper(API)
        end = time.time()
        print(f"Time: {end - start}")
