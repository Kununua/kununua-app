from django.core.management.base import BaseCommand
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
from scraper.utils.MatchingUtil import MatchingUtil

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        API = ScraperSQLiteAPI(name="scrapers_api.db")
        
        matcher = MatchingUtil(API.get_products_scraped(), API.get_packs_scraped())
        
        matcher.post_process_data_for_training()