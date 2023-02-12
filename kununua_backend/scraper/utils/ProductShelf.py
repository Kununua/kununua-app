import shelve, os
from products.models import Product, Category, Supermarket

class ProductShelf(object):
    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        
        self.path = path
        
        if not os.path.exists(self.path):
            self.shelf = shelve.open(self.path)
            self.shelf['supermarkets'] = {}
            self.shelf.close()
        else:
            self.shelf = shelve.open(self.path)
    
    def open(self):
        self.shelf = shelve.open(self.path)
        
    def close(self):
        self.shelf.close()
    
    def clear(self):
        self.open()
        self.shelf.clear()
        self.close()
        self.shelf = None
        
    def create_shelf(self, products):
        
        self._validate_creation_parameters(products)
            
        self.open()
        
        supermarkets = {product.supermarket.name for product in products}
        
        self._classify_products(products, supermarkets)
        
        for supermarket in supermarkets:
            self.shelf['supermarkets'][str(supermarket)] = supermarket
        
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
        
    def load_data_from_shelf(self, data_shelf):
        
        products = []
        
        for key in data_shelf:
            if key != 'supermarkets':
                products += data_shelf[key]
        
        self.create_shelf(products)
        self.close()
        
    def __str__(self):
        result = ''

        for key in self.shelf:
            result += "------------------ " + key.upper() + " ------------------" + '\n\n' + str([str(product) for product in self.shelf[key]][:20]) + '...\n------------------------------------------------------\n'
            
        return result
        
    # ------------------ Private methods ------------------ #
    
    def _validate_creation_parameters(self, products):
        if not isinstance(products, list):
            raise TypeError("products must be a list")
        
    def _classify_products(self, products, supermarkets):
        
        for supermarket in supermarkets:
            self.shelf[supermarket] = [product for product in products if product.supermarket.name == supermarket]
        
    # ------------------ Getters and setters ------------------ #
    
    def get_shelve(self):
        
        self.open()
        
        return self.shelf