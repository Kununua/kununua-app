from django.core.management.base import BaseCommand
from location.models import Country, Currency
from scraper.utils.ProductShelf import ProductShelf
import pandas as pd


class Command(BaseCommand):
    help = 'Populates the database with the products'

    def handle(self, *args, **options):
        
        print("Populating database with products...")
        
        shelve = ProductShelf(path="data/shelves/products")
        
        shelve.read_shelf()
        
        