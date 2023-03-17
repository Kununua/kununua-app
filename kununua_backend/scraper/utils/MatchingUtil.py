import json
from products.models import Product, Brand, Supermarket, Category
from location.models import Country
from data.functions.get_brands_list import get_brands_list
from scraper.models import ProductScraped, PackScraped
from scraper.utils.SimilarityCalculator import SimilarityCalculator
from data.similarities_threshold import THRESHOLDS, NAME_SIMILARITY_THRESHOLD
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI

class MatchingUtil(object):
    def __init__(self, sqlite_products):
        self.sqlite_products = sqlite_products
        self.similarity = SimilarityCalculator()
        self.packs_scraped = []
        self.supermarkets = []
        self.supermarkets_mapping = {}
        self.final_matches = []
        self.categories_mem = {}
        self.products_scraped = []
        
    def post_process_data(self):
        
        print("Phase 0: Loading supermarkets into postgres...")
        self._save_supermarkets()
        print("Phase 1: Parsing sqlite result to products objects...")
        self._parse_sqlite_products(self.sqlite_products)
        print("Phase 2: Performing brands matching...")
        self._brands_matching()
        print("Phase 3: Performing packs matching...")
        self._packs_matching()
        print("Phase 4: Performing categories matching...")
        self._categories_matching()
        print("Phase 5: Performing products matching...")
        self._products_matching()
        print(self.final_matches[:10])
        # print("Phase 6: Translating and injecting into postgres...")
        print("Done!")
        
        
    # ------------------------------- PRIVATE FUNCTIONS -------------------------------
    
    def _save_supermarkets(self):
        
        API = ScraperSQLiteAPI()
        
        supermarkets = API.get_supermarkets(condition="supermarkets.country = countries.id")
        
        for supermarket in supermarkets:
            pg_supermarket, _ = Supermarket.objects.get_or_create(name=supermarket[1], zipcode=supermarket[2], main_url=supermarket[3], country=Country.objects.get(code=supermarket[8]))
            self.supermarkets.append(pg_supermarket)
            self.supermarkets_mapping[supermarket[0]] = pg_supermarket.pk
        
    
    def _categories_matching(self):
        try:
            with open('data/categories.json', 'r', encoding='utf-8') as f:
                categories_dict = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("categories.json not found in: 'data/categories.json'")
        
        for product in self.products_scraped:
            
            category = self._parse_category(categories_dict[product.category])
            
            product.category = category
    
    @staticmethod
    def _parse_category(category):
        
        result = None
        category_splitted = category.split(">")
        
        for i in range(len(category_splitted)):
            if i > 0:
                result, _ = Category.objects.get_or_create(name=category_splitted[i], parent=Category.objects.get(name=category_splitted[i-1]))
            else:
                result, _ = Category.objects.get_or_create(name=category_splitted[i])
                
        return result
        
        
    def _products_matching(self):
        products = self.products_scraped
        
        if not products:
            return None
        
        if len(self.supermarkets) == 1:
            return products
            
        self.final_matches = self._get_matching_of_products(products)
    
    def _is_match(self, product1, product2):
        if product1.supermarket != product2.supermarket or self._get_root_category(product1.category) != self._get_root_category(product2.category) or product1.brand != product2.brand:
            return False
        
        name_similarity = self.similarity.compute_string_similarity(product1.name.lower().strip(), product2.name.lower().strip())
        
        if name_similarity > NAME_SIMILARITY_THRESHOLD:
            print(f"Product: {product1}; Matching: {product2}")
            print(f"Name similarity: {name_similarity};")
            return True
        
        return False
    
    def _get_root_category(self, category, old_categories=None):
        if category in self.categories_mem:
            if old_categories:
                for old_category in old_categories:
                    self.categories_mem[old_category] = self.categories_mem[category]
            return self.categories_mem[category]

        old_categories = old_categories or []
        
        if category.parent:
            old_categories.append(category)
            self._get_root_category(category.parent, old_categories)
        
        for old_category in old_categories:
            self.categories_mem[old_category] = category
        
        return category
        
    def _get_matching_of_products(self, products):
        
        result = []
        
        while True:
            
            if not products:
                break
            
            product = products.pop(0)
            
            matchings_of_product = self._get_matchings_of_products_recursive(product, products)
            result.append(matchings_of_product)
        
        return result

    def _get_matchings_of_products_recursive(self, product, products):
        
        result = [product]
        products_aux = products.copy()
        aux_index = 0
        
        while True:
            
            if not products_aux or aux_index >= len(products_aux):
                break
            
            product_to_compare = products_aux[aux_index]
            
            if self._is_match(product, product_to_compare):
                result.append(product_to_compare)
                products_aux.remove(products_aux.index(product_to_compare))
                result += self._get_matchings_of_products_recursive(product_to_compare, products_aux)
                products_aux = list(set(products_aux) - set(result))
                aux_index = 0
            else:
                aux_index += 1
                
        return result
                    
    def _brands_matching(self):
        """
        input: list of ProductScraped with ProductScraped.brand being None or a string
        output: list of ProductScraped with ProductScraped.brand being a Brand object or None
        """
        
        result = []
        
        for product in self.products_scraped:
            if product.brand:
                brand, new = Brand.objects.get_or_create(name__iexact=product.brand, defaults={'name': product.brand})
                if new:
                    with open('data/datasets/clean/brands.csv', 'w') as f:
                        f.write(f"{product.brand}\n")
                
                product.brand = brand
                
                result.append(product)
            
            else:
                brands = get_brands_list("data/datasets/clean/brands.csv")
                
                for brand in brands:
                    
                    if brand.lower() in product.name.lower():
                        pg_brand, new = Brand.objects.get_or_create(name__iexact=brand, defaults={'name': brand})
                        if new:
                            with open('data/datasets/clean/brands.csv', 'w') as f:
                                f.write(f"{product.brand}\n")
                        product.brand = pg_brand
                        result.append(product)
                        break
                    
        self.products_scraped = result
    
    def _packs_matching(self):
        
        products_to_return = []
        packs_to_return = []
        
        for supermarket in self.supermarkets:
            
            products_to_add = []
            packs_to_add = []
            
            supermarket_products = [product for product in self.products_scraped if product.supermarket.name == supermarket.name and product.supermarket.zipcode == supermarket.zipcode]
            
            for product in supermarket_products:
                
                if product.is_pack:
                    product_of_pack_id = self._search_product_of_pack_id(product, supermarket_products)
                    
                    if product_of_pack_id is not None:
                        packs_to_add.append(PackScraped(product_scraped=product_of_pack_id, amount=int(product.weight.split(' ')[0]), price=product.price, weight=product.weight.split("x")[1].replace(' ', ''), image=product.image, url=product.url))
                        continue
                
                products_to_add.append(product)
                
            #if supermarket not in self.shelf:
            products_to_return += products_to_add
            packs_to_return += packs_to_add
            
        self.products_scraped = products_to_return
        self.packs_scraped = packs_to_return
        
    
            
    def _search_product_of_pack_id(self, product, supermarket_products):
        
        match = None
        highest_similarity = 0
        for product_to_compare in supermarket_products:
            
            similarity_coef = self.similarity.compute_string_similarity(product_to_compare.name, product.name)
            try:
                if product_to_compare.category == product.category and product_to_compare.supermarket.name == product.supermarket.name and product_to_compare.is_pack == False and similarity_coef > highest_similarity: #and product_to_compare.weight in product.weight:
                    highest_similarity = similarity_coef
                    match = product_to_compare
            except Exception:
                print(f"Error en la comparación de productos con el producto {product} y el producto a comparar {product_to_compare}")

        return match.pseudo_id if match is not None else None
    
    def _parse_sqlite_products(self, sqlite_products):
        
        self.products_scraped =  [ProductScraped(
                                            pseudo_id = int(product[0]),
                                            name=str(product[1]),
                                            price=float(product[2]),
                                            unit_price=str(product[3]) if product[3] else None,
                                            weight=str(product[4]) if product[4] else None,
                                            brand=str(product[5]) if product[5] else None,
                                            amount=int(product[6]) if product[6] else None,
                                            image=str(product[7]),
                                            offer_price=float(product[8]) if product[8] else None,
                                            is_vegetarian=bool(product[9]),
                                            is_gluten_free=bool(product[10]),
                                            is_freezed=bool(product[11]),
                                            is_from_country=bool(product[12]),
                                            is_eco=bool(product[13]),
                                            is_without_sugar=bool(product[14]),
                                            is_without_lactose=bool(product[15]),
                                            url=str(product[16]) if product[16] else None,
                                            is_pack=bool(product[17]),
                                            category=str(product[18]),
                                            supermarket=Supermarket.objects.get(pk=self.supermarkets_mapping[int(product[19])]),
                                            )
                                        for product in sqlite_products
                                    ]