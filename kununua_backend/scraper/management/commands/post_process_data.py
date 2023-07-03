from django.core.management.base import BaseCommand
from location.models import Country, Currency
from scraper.scrapers.spain import scraper_el_jamon
from scraper.scrapers.spain import scraper_mercadona
from scraper.scrapers.spain import scraper_carrefour
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
from scraper.utils.MatchingUtil import MatchingUtil
import pandas as pd

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        API = ScraperSQLiteAPI("scrapers_api.db")
        
        matcher = MatchingUtil(API.get_products_scraped(), API.get_packs_scraped())
        
        matcher.post_process_data()