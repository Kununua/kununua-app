from django.db import models
from products.models import Category, Supermarket

class ProductScraped(object):
    
    def __init__(self, name=None, price=None, unit_price=None, brand=None, image=None, offer_price=None, 
                 is_vegetarian=False, is_gluten_free=False, 
                 is_freezed=False, is_from_country=False, is_eco=False, 
                 is_without_sugar=False, is_without_lactose=False, url=None, category=None, 
                 supermarket=None):
        
        if type(name) is not str:
            raise ValueError("Product name cannot be None and must be a string")
        if type(price) is not float:
            raise ValueError("Product price cannot be None and must be a float")
        if type(unit_price) is not str:
            raise ValueError("Product unit_price cannot be None and must be a string")
        if type(brand) is not str:
            raise ValueError("Product brand cannot be None and must be a string")
        if type(image) is not str:
            raise ValueError("Product image cannot be None and must be a string")
        if offer_price is not None and type(offer_price) is not float:
            raise ValueError("Product offer_price must be None or float")
        if type(is_vegetarian) is not bool:
            raise ValueError("Product is_vegetarian cannot be None and must be a boolean")
        if type(is_gluten_free) is not bool:
            raise ValueError("Product is_gluten_free cannot be None and must be a boolean")
        if type(is_freezed) is not bool:
            raise ValueError("Product is_freezed cannot be None and must be a boolean")
        if type(is_from_country) is not bool:
            raise ValueError("Product is_from_country cannot be None and must be a boolean")
        if type(is_eco) is not bool:
            raise ValueError("Product is_eco cannot be None and must be a boolean")
        if type(is_without_sugar) is not bool:
            raise ValueError("Product is_without_sugar cannot be None and must be a boolean")
        if type(is_without_lactose) is not bool:
            raise ValueError("Product is_without_lactose cannot be None and must be a boolean")
        if type(url) is not str:
            raise ValueError("Product url cannot be None and must be a string")
        if type(category) is not Category:
            raise ValueError("Product category cannot be None and must be a Category object")
        if type(supermarket) is not Supermarket:
            raise ValueError("Product supermarket cannot be None and must be a Supermarket object")
        
        
        self.name = name
        self.price = price
        self.unit_price = unit_price
        self.brand = brand
        self.image = image
        self.offer_price = offer_price
        self.is_vegetarian = is_vegetarian
        self.is_gluten_free = is_gluten_free
        self.is_freezed = is_freezed
        self.is_from_country = is_from_country
        self.is_eco = is_eco
        self.is_without_sugar = is_without_sugar
        self.is_without_lactose = is_without_lactose
        self.url = url
        self.category = category
        self.supermarket = supermarket
        
    def __str__(self):
        return f"Product[name: {self.name}, price: {self.price}, unit_price: {self.unit_price}, brand: {self.brand}, offer_price: {self.offer_price}, category: {self.category.name}, supermarket: {self.supermarket.name}]"