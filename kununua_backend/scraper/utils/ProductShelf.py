import shelve, os
from products.models import Product, Category, Supermarket

class ProductShelf(object):
    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        
        self.path = path
        self.shelf = None
    
    def open(self):
        self.shelf = shelve.open(self.path)
        
    def close(self):
        self.shelf.close()
    
    def clear(self):
        self.open()
        self.shelf.clear()
        self.close()
        self.shelf = None
        
    def create_shelf(self, supermarket, categories, products):
        if not isinstance(supermarket, Supermarket):
            raise TypeError("supermarket must be a string")
        if not isinstance(categories, list):
            raise TypeError("categories must be a list")
        if not isinstance(products, list):
            raise TypeError("products must be a list")
        data = zip(categories, products)
        is_new = False
        if not os.path.exists(self.path):
            is_new = True
            
        self.open()
        self.shelf[supermarket.name] = data
        
        if is_new:
            self.shelf['supermarkets'] = {}
            
        supermarkets = self.shelf['supermarkets']
        supermarkets[supermarket.name] = supermarket
        self.shelf['supermarkets'] = supermarkets
        
        self.close()

    def read_shelf(self):
        self.open()
        products = []
        for key in self.shelf:
            if key != 'supermarkets': 
                elements = self.shelf[key]
                supermarket = self.shelf['supermarkets'][key]
                try:
                    supermarket, _ = Supermarket.objects.get_or_create(name=supermarket.name, country=supermarket.country, zipcode=supermarket.zipcode, main_url=supermarket.main_url)
                    for category, product in elements:
                        if not Product.objects.filter(url=product.url).exists():
                            category_name = category.name if isinstance(category, Category) else category
                            category, _ = Category.objects.get_or_create(name=category_name)
                            product.category = category
                            product.supermarket = supermarket
                            products.append(product)
                except ValueError:
                    print("Error creando los productos")
                    
        Product.objects.bulk_create(products)
        
        self.close()
                