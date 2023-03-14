import SQLiteAPI, os
from django.utils.translation import gettext as _
from models import ProductScraped, PackScraped
from products.models import Supermarket
from location.models import Country, Currency

DB_PATH = os.path.join("kununua_backend", "data", "db", "scraper.db")
PRODUCT_TABLE_NAME = "productsScraped"
PACK_TABLE_NAME = "packsScraped"
CURRENCY_TABLE_NAME = "currencies"
COUNTRY_TABLE_NAME = "countries"
SUPERMARKET_TABLE_NAME = "supermarkets"

class ScraperSQLiteAPI(SQLiteAPI):
    
    def __init__(self):
        if not isinstance(DB_PATH, str):
            raise ValueError(_("Database name must be a string"))
        dir_path = DB_PATH[:DB_PATH.rfind(os.path.sep)]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        super().__init__(DB_PATH)
        self.create_table(CURRENCY_TABLE_NAME, "name TEXT NOT NULL, code TEXT NOT NULL, symbol TEXT, PRIMARY KEY(name, code)")
        self.create_table(COUNTRY_TABLE_NAME, "spanish_name TEXT NOT NULL, english_name TEXT NOT NULL, code TEXT NOT NULL, phone_code TEXT, currency TEXT NOT NULL, PRIMARY KEY(spanish_name, english_name, code), FOREIGN KEY(currency) REFERENCES currencies(name, code))")
        self.create_table(SUPERMARKET_TABLE_NAME, "name TEXT NOT NULL, zipcode TEXT NOT NULL, main_url TEXT NOT NULL, country TEXT NOT NULL, PRIMARY KEY(name, zipcode, main_url, country), FOREIGN KEY(country) REFERENCES countries(spanish_name, english_name, code))")
        self.create_table(PRODUCT_TABLE_NAME, "pseudo_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price REAL NOT NULL, unit_price TEXT, weight TEXT, brand TEXT, amount INTEGER, image TEXT NOT NULL, offer_price REAL, is_vegetarian INTEGER NOT NULL, is_gluten_free INTEGER NOT NULL, is_freezed INTEGER NOT NULL, is_from_country INTEGER NOT NULL, is_eco INTEGER NOT NULL, is_without_sugar INTEGER NOT NULL, is_without_lactose INTEGER NOT NULL, url TEXT, is_pack INTEGER NOT NULL, category TEXT NOT NULL, supermarket TEXT NOT NULL, FOREIGN KEY(supermarket) REFERENCES supermarkets(name, zipcode, main_url, country)")
        self.create_table(PACK_TABLE_NAME, "product_id INTEGER NOT NULL, amount INTEGER NOT NULL, price REAL NOT NULL, weight TEXT, image TEXT NOT NULL, url TEXT, FOREIGN KEY(product_id) REFERENCES productsScraped(pseudo_id)")
        
    def add_products_scraped(self, products):
        if not isinstance(products, list):
            raise ValueError(_("Products must be a list"))
        for product in products:
            self._add_product(product)
    
    def _add_product_scraped(self, product):
        if not isinstance(product, ProductScraped):
            raise ValueError(_("Product must be a ProductScraped object"))
        self.insert(PRODUCT_TABLE_NAME, product.__dict__)
    
    def add_packs_scraped(self, packs):
        if not isinstance(packs, list):
            raise ValueError(_("Packs must be a list"))
        for pack in packs:
            self._add_pack(pack)
        
    def _add_pack_scraped(self, pack):
        if not isinstance(pack, PackScraped):
            raise ValueError(_("Pack must be a PackScraped object"))
        self.insert(PACK_TABLE_NAME, pack.__dict__)
    
    def add_supermarkets(self, supermarkets):
        if not isinstance(supermarkets, list):
            raise ValueError(_("Supermarkets must be a list"))
        for supermarket in supermarkets:
            self._add_supermarket(supermarket)
    
    def _add_supermarket(self, supermarket):
        if not isinstance(supermarket, Supermarket):
            raise ValueError(_("Supermarket must be a Supermarket object"))
        self.insert(SUPERMARKET_TABLE_NAME, supermarket.__dict__)
    
    def add_countries(self, countries):
        if not isinstance(countries, list):
            raise ValueError(_("Countries must be a list"))
        for country in countries:
            self._add_country(country)
    
    def _add_country(self, country):
        if not isinstance(country, Country):
            raise ValueError(_("Country must be a Country object"))
        self.insert(COUNTRY_TABLE_NAME, country.__dict__)
    
    def add_currencies(self, currencies):
        if not isinstance(currencies, list):
            raise ValueError(_("Currencies must be a list"))
        for currency in currencies:
            self._add_currency(currency)
    
    def _add_currency(self, currency):
        if not isinstance(currency, Currency):
            raise ValueError(_("Currency must be a Currency object"))
        self.insert(CURRENCY_TABLE_NAME, currency.__dict__)
