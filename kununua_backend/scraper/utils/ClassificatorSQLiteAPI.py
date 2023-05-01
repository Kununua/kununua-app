import os, json
from django.utils.translation import gettext as _
from scraper.utils.SQLiteAPI import SQLiteAPI
from scraper.models import ProductScraped

DB_PATH = os.path.join("data", "db", "classificator.db")
PRODUCT_TABLE_NAME = "productsScraped"
MATCH_TABLE_NAME = "matches"

class ClassificatorSQLiteAPI(SQLiteAPI):
    
    def __init__(self):
        if not isinstance(DB_PATH, str):
            raise ValueError(_("Database name must be a string"))
        dir_path = DB_PATH[:DB_PATH.rfind(os.path.sep)]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        super().__init__(DB_PATH)
        self.create_table(PRODUCT_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price REAL NOT NULL, unit_price TEXT, weight TEXT, brand TEXT, amount INTEGER, image TEXT NOT NULL, offer_price REAL, is_vegetarian INTEGER NOT NULL, is_gluten_free INTEGER NOT NULL, is_freezed INTEGER NOT NULL, is_from_country INTEGER NOT NULL, is_eco INTEGER NOT NULL, is_without_sugar INTEGER NOT NULL, is_without_lactose INTEGER NOT NULL, url TEXT, is_pack INTEGER NOT NULL, category TEXT NOT NULL, supermarket TEXT NOT NULL")
        self.create_table(MATCH_TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, product1 INTEGER NOT NULL, product2 INTEGER NOT NULL, is_match INTEGER, FOREIGN KEY(product1) REFERENCES productsScraped(id), FOREIGN KEY(product2) REFERENCES productsScraped(id)")

    def add_products_scraped(self, products):
        if not isinstance(products, list):
            raise ValueError(_("Products must be a list"))
        
        for product in products:
            self._add_product_scraped(product)
    
    def _add_product_scraped(self, product):
        if not isinstance(product, ProductScraped):
            raise ValueError(_("Product must be a ProductScraped object"))
        data = f"""
            {self._parse_str(product.name)}, 
            {self._handle_none(product.price)}, 
            {self._parse_str(product.unit_price)}, 
            {self._parse_str(product.weight)}, 
            {self._parse_str(product.brand.name if product.brand else product.brand)}, 
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
            {self._parse_str(product.category.name)},
            {self._parse_str(product.supermarket.name)}
            """
        columns = "(name, price, unit_price, weight, brand, amount, image, offer_price, is_vegetarian, is_gluten_free, is_freezed, is_from_country, is_eco, is_without_sugar, is_without_lactose, url, is_pack, category, supermarket)"
        
        self.insert_data(PRODUCT_TABLE_NAME + columns, data)
    
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
    
    @staticmethod
    def _parse_is_match(is_match):
        if is_match is not None:
            if is_match == "True":
                return 1
            return 0
        return "null"

    def get_products_scraped(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(PRODUCT_TABLE_NAME, columns, condition)
    
    def get_possible_matches(self, columns="*", condition=None):
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        if condition is not None and not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        return self.select_data(MATCH_TABLE_NAME, columns, condition)
    
    def add_match(self, product1, product2, is_match):
        if not product1:
            raise ValueError(_("Product1 must exists"))
        if not product2:
            raise ValueError(_("Product2 must exists"))
        
        if product1 == product2:
            raise ValueError(_("Product1 and Product2 must be different"))
        
        if isinstance(product1, ProductScraped):
            product1 = product1.pseudo_id
        if isinstance(product2, ProductScraped):
            product2 = product2.pseudo_id
        
        if not isinstance(product1, int):
            raise TypeError(_("Product1 must be an int"))
        if not isinstance(product2, int):
            raise TypeError(_("Product2 must be an int"))
        
        columns = "(product1, product2, is_match)"
        return self.insert_data(MATCH_TABLE_NAME+columns, f"{product1}, {product2}, {self._parse_is_match(is_match)}")

    def update_match(self, product1_id, product2_id, is_match):
        return self.update_data(MATCH_TABLE_NAME, f"is_match={self._parse_is_match(is_match)}", f"product1={product1_id} AND product2={product2_id}")