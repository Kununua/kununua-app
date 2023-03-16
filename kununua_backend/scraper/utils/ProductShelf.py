import shelve, os, json
from products.models import Product, Category, Supermarket
from location.models import Country
from .SimilarityCalculator import SimilarityCalculator as sm
from ..models import PackScraped
from data.similarities_threshold import THRESHOLDS
from data.synonyms import CategoryFinder as cf

CategoryFinder = cf()
SimilarityCalculator = sm()
class ProductShelf(object):
    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        
        self.path = path
        
        if not os.path.exists(self.path):
            self.open()
            self.shelf['supermarkets'] = {}
            self.close()
    
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
            
        self._update_json_categories(products)
        
        self.close()

    def read_shelf(self):
        self.open()
        self._get_matchings()
                
        self.close()
    
    def _get_matchings(self):
        products = []
        while True:
            keys = [key for key in self.shelf.keys() if key != 'supermarkets']
            if not keys or len(keys)==1:
                break
            first_key = keys[0]
            keys.remove(first_key)
            for product in  self.shelf[first_key]["products"]:
                if product in products:
                    continue
                has_match = False
                matchings = []
                for key in keys:
                    #products_per_category = [product for product in self.shelf[key]["products"] if product.category == product.category]
                    for product_to_compare in self.shelf[key]['products']:
                        # if product_to_compare.category != product.category:
                        #     continue
                        if product_to_compare in products:
                            continue
                        name_similarity = SimilarityCalculator.compute_string_similarity(product.name.lower().strip(), product_to_compare.name.lower().strip())
                        weight_similarity = None
                        brand_similarity = None
                        
                        if product.weight and product_to_compare.weight:
                            weight_similarity = SimilarityCalculator.compute_string_similarity(product.weight.replace(" ", "").lower().strip(), product_to_compare.weight.replace(" ", "").lower().strip())

                        if product.brand and product_to_compare.brand:
                            brand_similarity = SimilarityCalculator.compute_string_similarity(product.brand.lower().strip(), product_to_compare.brand.lower().strip())
                            
                        if name_similarity > 0.8 and (weight_similarity==None or weight_similarity > 0.8) and (brand_similarity==None or brand_similarity > 0.8):
                            print(f"Product: {product}; Matching: {product_to_compare}")
                            print(f"Name similarity: {name_similarity}; Weight similarity: {weight_similarity}; Brand similarity: {brand_similarity}")
                            products.append(product_to_compare)
                            matchings.append(product_to_compare)
                            has_match = True
                            print("#"*50)
                            break
                if has_match:
                    #Product.objects.create(name=product.name, brand=product.brand, image=product.image, category=product.category)
                    products.append(product)
    
    def _create_supermarket(self, key):
        supermarket = None
        if Supermarket.objects.filter(name=key).exists():
            supermarket = Supermarket.objects.get(name=key)
        else:
            main_url = "https://www."+key.lower().replace(" ", "").strip()+".es" if "El Jamón" not in key else "https://www.supermercadoseljamon.com"
            supermarket = Supermarket.objects.create(name=key, zipcode="41009", main_url=main_url, country=Country.objects.get(name="Spain"))
        
        return supermarket
        
    def load_data_from_shelf(self, data_shelf):
        
        products = []
        
        for key in data_shelf:
            if key != 'supermarkets':
                products += data_shelf[key]
        
        data_shelf.close()
        
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
        
    def _update_json_categories(self, products):
        categories_to_translate = {product.category.name for product in products}
        
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
                        packs_to_add.append(PackScraped(product_id=product_of_pack_id, amount=None, price=product.price, weight=product.weight, image=product.image, url=product.url))
                        continue
                
                product.pseudo_id = next_pseudo_id
                products_to_add.append(product)
                next_pseudo_id += 1
                
            #if supermarket not in self.shelf:
            self.shelf[supermarket] = {"products": products_to_add, "packs": packs_to_add}
            
    def _search_product_of_pack_id(self, product, supermarket_products, similarity_calculator, supermarket):
        
        match = None
        highest_similarity = 0
        for product_to_compare in supermarket_products:
            
            similarity_coef = similarity_calculator.compute_string_similarity(product_to_compare.name, product.name)
            try:
                if product_to_compare.category.name == product.category.name and product_to_compare.supermarket.name == product.supermarket.name and product_to_compare.is_pack == False and similarity_coef > highest_similarity: #and product_to_compare.weight in product.weight:
                    highest_similarity = similarity_coef
                    match = product_to_compare
            except Exception:
                print(f"Error en la comparación de productos con el producto {product} y el producto a comparar {product_to_compare}")
                
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