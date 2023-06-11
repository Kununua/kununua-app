import os, json
from django.utils.translation import gettext as _
from scraper.utils.SQLiteAPI import SQLiteAPI
from scraper.models import ProductScraped
from location.models import Currency
import pandas as pd

PRODUCT_TABLE_NAME = "productsScraped"
PACK_TABLE_NAME = "packsScraped"
CURRENCY_TABLE_NAME = "currencies"
COUNTRY_TABLE_NAME = "countries"
SUPERMARKET_TABLE_NAME = "supermarkets"
MERCADONA_CATEGORIES_CACHE = "mercCache"

class ScraperSQLiteAPI(SQLiteAPI):
    
    def __init__(self, name=None):

        if not name:
            raise ValueError(_("Database name is required"))
        
        db_path = os.path.join("data", "db", name)        

        if not isinstance(db_path, str):
            raise ValueError(_("Database name must be a string"))
        
        dir_path = db_path[:db_path.rfind(os.path.sep)]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        super().__init__(db_path)
        self.create_table(CURRENCY_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, code TEXT NOT NULL, symbol TEXT")
        self.create_table(COUNTRY_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, spanish_name TEXT NOT NULL, english_name TEXT NOT NULL, code TEXT NOT NULL, phone_code TEXT, currency INTEGER NULL, FOREIGN KEY(currency) REFERENCES currencies(id)")
        self.create_table(SUPERMARKET_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, zipcode TEXT NOT NULL, main_url TEXT NOT NULL, country INTEGER NOT NULL, FOREIGN KEY(country) REFERENCES countries(id)")
        self.create_table(PRODUCT_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, ean TEXT, price REAL NOT NULL, unit_price TEXT, weight TEXT, brand TEXT, amount INTEGER, image TEXT NOT NULL, offer_price REAL, is_vegetarian INTEGER NOT NULL, is_gluten_free INTEGER NOT NULL, is_freezed INTEGER NOT NULL, is_from_country INTEGER NOT NULL, is_eco INTEGER NOT NULL, is_without_sugar INTEGER NOT NULL, is_without_lactose INTEGER NOT NULL, url TEXT, is_pack INTEGER NOT NULL, category TEXT NOT NULL, supermarket INTEGER NOT NULL, FOREIGN KEY(supermarket) REFERENCES supermarkets(id)")
        self.create_table(PACK_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, price REAL NOT NULL, weight TEXT, image TEXT NOT NULL, url TEXT, product_scraped INTEGER NOT NULL, FOREIGN KEY(product_scraped) REFERENCES productsScraped(id)")
        if name == "mercadona_cache.db":
            self.create_table(MERCADONA_CATEGORIES_CACHE, "id INTEGER PRIMARY KEY AUTOINCREMENT, counter INTEGER NOT NULL")

        if self.select_data(COUNTRY_TABLE_NAME, "COUNT(*)", None)[0][0] == 0:
            self._populate_initial_data()

        if name == "mercadona_cache.db" and self.select_data(MERCADONA_CATEGORIES_CACHE, "COUNT(*)", None)[0][0] == 0:
            self._populate_mercadona_categories_cache()
        
    def _populate_initial_data(self):
        def get_attr(country, key):
            return country[key] if country[key] != 'None' else None
        
        countries = pd.read_csv('data/datasets/clean/cleaned-countries.csv', sep=';')

        for _, country in countries.iterrows():
            currency_id = None
            if get_attr(country, 'currency_name') and get_attr(country, 'currency_code'):
                currency_data = Currency(name=get_attr(country, 'currency_name'), code=get_attr(country, 'currency_code'), symbol=get_attr(country, 'currency_symbol'))
                currency_id = self._add_currency(currency_data)

            country = {'spanish_name':get_attr(country, 'spanish_name'), 'english_name':get_attr(country, 'english_name'), 'code':get_attr(country, 'iso3'), 'phone_code':get_attr(country, 'phone_code'), 'currency':currency_id}
            self._add_country(country)

    def _populate_mercadona_categories_cache(self):
        self.insert_data(MERCADONA_CATEGORIES_CACHE+"(counter)", "0")

    def add_products_scraped(self, products):
        if not isinstance(products, list):
            raise ValueError(_("Products must be a list"))
        
        self._update_json_categories(products)
        for product in products:
            self._add_product_scraped(product)
    
    def _add_product_scraped(self, product):
        if not isinstance(product, ProductScraped):
            raise ValueError(_("Product must be a ProductScraped object"))
        data = f"""
            {self._parse_str(product.name)}, 
            {self._parse_str(product.ean)}, 
            {self._handle_none(product.price)}, 
            {self._parse_str(product.unit_price)}, 
            {self._parse_str(product.weight)}, 
            {self._parse_str(product.brand)}, 
            {self._handle_none(product.amount)}, 
            {self._parse_str(product.image)}, 
            {self._handle_none(product.offer_price)},
            {self._parse_flag(product.is_vegetarian)}, 
            {self._parse_flag(product.is_gluten_free)}, 
            {self._parse_flag(product.is_freezed)}, 
            {self._parse_flag(product.is_from_country)}, 
            {self._parse_flag(product.is_eco)}, 
            {self._parse_flag(product.is_without_sugar)}, 
            {self._parse_flag(product.is_without_lactose)}, 
            {self._parse_str(product.url)}, 
            {self._parse_flag(product.is_pack)}, 
            {self._parse_str(product.category)},
            {self.select_data(SUPERMARKET_TABLE_NAME, "id", f"name = {self._parse_str(product.supermarket.name)} AND zipcode = {self._parse_str(product.supermarket.zipcode)}")[0][0]}
            """
        columns = "(name, ean, price, unit_price, weight, brand, amount, image, offer_price, is_vegetarian, is_gluten_free, is_freezed, is_from_country, is_eco, is_without_sugar, is_without_lactose, url, is_pack, category, supermarket)"
        
        self.insert_data(PRODUCT_TABLE_NAME + columns, data)
        
    def _update_json_categories(self, products):
        categories_to_translate = {product.category for product in products}
        
        try:
            with open('data/categories.json', 'r', encoding='utf-8') as f:
                categories_dict = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("categories.json not found in: 'data/categories.json'")
        
        categories_to_translate = categories_to_translate.union(set(categories_dict.keys()))
        new_categories_dict = {}
        
        for category in sorted(categories_to_translate):
            if category not in categories_dict:
                new_categories_dict[category.lower().capitalize()] = ''
            else:
                new_categories_dict[category] = categories_dict[category]
                
        os.remove('data/categories.json')
        
        new_categories_json = json.dumps(new_categories_dict, indent=4, ensure_ascii=False)
        
        with open('data/categories.json', 'w', encoding='utf-8') as f:
            f.write(new_categories_json)
    
    @staticmethod
    def _parse_flag(flag):
        if flag:
            return 1
        return 0
    
    @staticmethod
    def _parse_str(string):
        if string is not None:
            clean_string = str(string).replace("'", "").strip()
            return f"'{clean_string}'"
        return "null"

    @staticmethod
    def _handle_none(value):
        if value is not None:
            return str(value)
        return "null"
    
    def add_supermarkets(self, supermarkets):
        if not isinstance(supermarkets, list):
            raise ValueError(_("Supermarkets must be a list"))
        for supermarket in supermarkets:
            self._add_supermarket(supermarket)
    
    def _add_supermarket(self, supermarket):
        if not isinstance(supermarket, dict):
            raise ValueError(_("Supermarket must be a dict"))
        data = f"""
        {self._parse_str(supermarket['name'])},
        {self._parse_str(supermarket['zipcode'])},
        {self._parse_str(supermarket['main_url'])},
        {self._get_country(supermarket['country'])}
        """
        columns = "(name, zipcode, main_url, country)"
        
        self.insert_data(SUPERMARKET_TABLE_NAME+columns, data)
    
    def _get_country(self, country_code):
        country = self.select_data(COUNTRY_TABLE_NAME, "id", f"code = {self._parse_str(country_code)}")
        if len(country) == 0:
            raise ValueError(_("Country not found"))
        return country[0][0]
    
    def add_countries(self, countries):
        if not isinstance(countries, list):
            raise ValueError(_("Countries must be a list"))
        for country in countries:
            self._add_country(country)
    
    def _add_country(self, country):
        if not isinstance(country, dict):
            raise ValueError(_("Country must be a dict"))
        data = f"""
        {self._parse_str(country['spanish_name'])},
        {self._parse_str(country['english_name'])},
        {self._parse_str(country['code'])},
        {self._parse_str(country['phone_code'])},
        {self._handle_none(country['currency'])}
        """
        columns = "(spanish_name, english_name, code, phone_code, currency)"
        self.insert_data(COUNTRY_TABLE_NAME+columns, data)
    
    def add_currencies(self, currencies):
        if not isinstance(currencies, list):
            raise ValueError(_("Currencies must be a list"))
        for currency in currencies:
            self._add_currency(currency)
    
    def _add_currency(self, currency):
        if not isinstance(currency, Currency):
            raise ValueError(_("Currency must be a Currency object"))
        
        columns = "(name, code, symbol)"
    
        result = self.select_data(CURRENCY_TABLE_NAME, "id", f"name = {self._parse_str(currency.name)}")
        if result:
            return int(result[0][0])
        
        self.insert_data(CURRENCY_TABLE_NAME + columns, f"{self._parse_str(currency.name)}, {self._parse_str(currency.code)}, {self._parse_str(currency.symbol)}")
        
        return int(self.select_data(CURRENCY_TABLE_NAME, "id", f"name = {self._parse_str(currency.name)}")[0][0])

    def get_products_scraped(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(PRODUCT_TABLE_NAME, columns, condition)

    def get_packs_scraped(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(PACK_TABLE_NAME, columns, condition)
    
    def get_supermarkets(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(SUPERMARKET_TABLE_NAME + " LEFT JOIN " + COUNTRY_TABLE_NAME, columns, condition)

    def get_countries(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(COUNTRY_TABLE_NAME, columns, condition)
    
    def get_currencies(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(CURRENCY_TABLE_NAME, columns, condition)