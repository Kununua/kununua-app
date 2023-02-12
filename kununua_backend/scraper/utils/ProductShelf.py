import shelve, os
from products.models import Product, Category, Supermarket
from .SimilarityCalculator import SimilarityCalculator
from ..models import PackScrapped
from data.similarities_threshold import THRESHOLDS

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
        
        next_pseudo_id = self._get_next_pseudo_id()
        
        supermarkets = {product.supermarket.name for product in products}
        
        #self._standard_save(products, supermarkets)
        self._classify_products(products, supermarkets, next_pseudo_id)
        
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
        
    def _get_next_pseudo_id(self):
        
        highest_pseudo_ids = []
        
        for key in self.shelf:
            if key != 'supermarkets':
                try:
                    highest_pseudo_ids.append(max([product.pseudo_id for product in self.shelf[key]]))
                except Exception:
                    pass
        
        if len(highest_pseudo_ids) == 0:
            return 1
        else:
            return max(highest_pseudo_ids) + 1
        
    def _standard_save(self, products, supermarkets):
        
        for supermarket in supermarkets:
            self.shelf[str(supermarket)] = [product for product in products if product.supermarket.name == supermarket]
        
    def _classify_products(self, products, supermarkets, next_pseudo_id):
        
        similarity_calculator = SimilarityCalculator()
        
        for supermarket in supermarkets:
            
            products_to_add = []
            packs_to_add = []
            
            supermarket_products = [product for product in products if product.supermarket.name == supermarket]
            
            for product in supermarket_products:
                
                if product.is_pack:
                    product_of_pack_id = self._search_product_of_pack_id(product, supermarket_products, similarity_calculator, supermarket)
                    
                    if product_of_pack_id is not None:
                        packs_to_add.append(PackScrapped(product_id=product_of_pack_id, amount=None, price=product.price, weight=product.weight, image=product.image, url=product.url))
                        continue
                
                product.pseudo_id = next_pseudo_id
                products_to_add.append(product)
                next_pseudo_id += 1
            
            self.shelf[supermarket]['products'] = products_to_add
            self.shelf[supermarket]['packs'] = packs_to_add
            
    def _search_product_of_pack_id(self, product, supermarket_products, similarity_calculator, supermarket):
        
        match = None
        highest_similarity = 0
        for product_to_compare in supermarket_products:
            
            similarity_coef = similarity_calculator.compute_string_similarity(product_to_compare.name, product.name)
            
            if product_to_compare.category.name == product.category.name and product_to_compare.supermarket.name == product.supermarket.name and product_to_compare.is_pack == False and similarity_coef > highest_similarity and product_to_compare.weight in product.weight:
                highest_similarity = similarity_coef
                match = product_to_compare
                
        if highest_similarity > THRESHOLDS[supermarket]:
            print(f"'{product.name}' single product is: '{match.name} ({match.weight})' ({product.weight})")
        else:
            match = None
            
        if match is None:
            print(f"The pack {product.name} will be stored as a single product ({product.weight})")

        return match.pseudo_id if match is not None else None
        
        
    # ------------------ Getters and setters ------------------ #
    
    def get_shelve(self):
        
        self.open()
        
        return self.shelf