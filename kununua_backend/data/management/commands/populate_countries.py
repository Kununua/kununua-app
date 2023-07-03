from django.core.management.base import BaseCommand
from location.models import Country, Currency
import pandas as pd


class Command(BaseCommand):
    help = 'Populates the database with the countries'

    def handle(self, *args, **options):
        
        print("Populating database with countries...")
        
        def get_attr(country, key):
            return country[key] if country[key] != 'None' else None
        
        def add_countries_to_db():
            countries_to_add = []
            for index, country in countries.iterrows():
                
                currency = None
                
                if get_attr(country, 'currency_name') and get_attr(country, 'currency_code'):
                    currency, _ = Currency.objects.get_or_create(name=get_attr(country, 'currency_name'), code=get_attr(country, 'currency_code'), symbol=get_attr(country, 'currency_symbol'))
                
                countries_to_add.append(Country(spanish_name=get_attr(country, 'spanish_name'), english_name=get_attr(country, 'english_name'), code=get_attr(country, 'iso3'), phone_code=get_attr(country, 'phone_code'), currency=currency))
            
            Country.objects.bulk_create(countries_to_add)
    
        countries = pd.read_csv('data/datasets/clean/cleaned-countries.csv', sep=';')
        
        Currency.objects.all().delete()
        Country.objects.all().delete()
        
        if Country.objects.count() == 0 and Currency.objects.count() == 0:
            
            add_countries_to_db()
        
        else:
            print("There are already countries or currencies in the database. Please, clean the tables before populating them again.")