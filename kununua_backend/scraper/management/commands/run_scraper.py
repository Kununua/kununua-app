from django.core.management.base import BaseCommand
from location.models import Country, Currency
from scraper.scrapers.spain import scraper_el_jamon
from scraper.scrapers.spain import scraper_mercadona
from scraper.utils.ProductShelf import ProductShelf
import pandas as pd

class Command(BaseCommand):
        
    help = '--------------------------------------------------------\n--------------- SCRAPER LAUNCHER UTILITY ---------------\n--------------------------------------------------------\n'

    def handle(self, *args, **options):
        
        # scraper_el_jamon.scraper()
        
        shelve_util = ProductShelf('data/shelves/productos-copy2.dat')
        shelve_util.read_shelf()