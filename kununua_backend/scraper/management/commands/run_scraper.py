from django.core.management.base import BaseCommand
from location.models import Country, Currency
from scraper.scrapers.spain import scraper_el_jamon
from scraper.scrapers.spain import scraper_mercadona
from scraper.utils.ProductShelf import ProductShelf
import pandas as pd

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        shelve_util = ProductShelf('data/shelves/new-products-scraped')
        new_shelve_util = ProductShelf('data/shelves/new-shelve-classified')
        
        new_shelve_util.load_data_from_shelf(shelve_util.get_shelve())
        
        shelve_util.close()
        # new_shelve_util.open()
        # print(new_shelve_util)
        # new_shelve_util.close()