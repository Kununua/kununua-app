from django.core.management.base import BaseCommand
from products.models import Brand
from data.functions.get_brands_list import get_brands_list


class Command(BaseCommand):
    help = 'Populates the database with the supported brands'

    def handle(self, *args, **options):
        
        print("Populating database with brands...")
        
        def populate():
            
            brands_to_add = []
            
            for brand in get_brands_list("data/datasets/clean/brands.csv"):
                brands_to_add.append(Brand(name=brand))
            
            Brand.objects.bulk_create(brands_to_add)
        
        if Brand.objects.all().count() > 0:
            
            reset = input("Brands table is not empty. Do you want to reset it? (y/N) ")
            
            if reset.lower() != "y":
                return
            
        
        Brand.objects.all().delete()
        populate()