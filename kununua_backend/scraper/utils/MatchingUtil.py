import json, stanza
from products.models import Product, Brand, Supermarket, Category, Price
from location.models import Country
from data.functions.get_brands_list import get_brands_list
from scraper.models import ProductScraped, PackScraped
from scraper.utils.SimilarityCalculator import SimilarityCalculator
from data.similarities_threshold import THRESHOLDS, NAME_SIMILARITY_THRESHOLD
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
from scraper.utils.ClassificatorSQLiteAPI import ClassificatorSQLiteAPI

DISTANCE_UNITS = ["km", "m", "dm", "cm", "mm"]
VOLUME_UNITS = ["kl", "l", "dl", "cl", "ml"]
MASS_UNITS = ["kg", "g", "dg", "cg", "mg"]

class MatchingUtil(object):
    def __init__(self, sqlite_products):
        self.sqlite_products = sqlite_products
        self.classificator_api = ClassificatorSQLiteAPI()
        self.similarity = SimilarityCalculator()
        self.packs_scraped = []
        self.supermarkets = []
        self.supermarkets_mapping = {}
        self.final_matches = []
        self.categories_mem = {}
        self.products_scraped = []
        self.nlp = stanza.Pipeline('es')
        
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
        # print("Phase 6: Translating and injecting into postgres...")
        print("Done!")
        
    def post_process_data_for_training(self):
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
        print("Phase 5: Storing products in new db...")
        self._stores_data(self.products_scraped)
        print("Phase 6: Storing possible matches in new db...")
        self._stores_possible_matches()
        print("Done!")
        
        
        
    # ------------------------------- PRIVATE FUNCTIONS -------------------------------
    
    # ---------------------------- PHASE 0 ----------------------------
    
    def _save_supermarkets(self):
        
        API = ScraperSQLiteAPI()
        
        supermarkets = API.get_supermarkets(condition="supermarkets.country = countries.id")
        
        for supermarket in supermarkets:
            pg_supermarket, _ = Supermarket.objects.get_or_create(name=supermarket[1], zipcode=supermarket[2], main_url=supermarket[3], country=Country.objects.get(code=supermarket[8]))
            self.supermarkets.append(pg_supermarket)
            self.supermarkets_mapping[supermarket[0]] = pg_supermarket.pk
            
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 1 ----------------------------
    
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
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 2 ----------------------------
    
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
                    with open('data/datasets/clean/brands.csv', 'a') as f:
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
                else:
                    result.append(product)
                    
        self.products_scraped = result
     
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 3 ----------------------------
    
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
                        
                        try:
                            pack_amount = int(product.weight.split(' ')[0])
                        except Exception:
                            pack_amount = 1
                            
                        try:
                            pack_weight = product.weight.split("x")[1].replace(' ', '')
                        except Exception:
                            pack_weight = ''
                        
                        packs_to_add.append(PackScraped(product_scraped=product_of_pack_id, amount=pack_amount, price=product.price, weight=pack_weight, image=product.image, url=product.url))
                        continue
                
                products_to_add.append(product)
            
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
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 4 ----------------------------
    
    def _categories_matching(self):
        try:
            with open('data/categories.json', 'r', encoding='utf-8') as f:
                categories_dict = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("categories.json not found in: 'data/categories.json'")
        
        for product in self.products_scraped:
            
            category = self._parse_category(categories_dict[product.category.lower().strip().capitalize()])
            
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
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 5 ----------------------------
    
    def _products_matching(self):
        products = self.products_scraped
        
        if not products:
            self.final_matches = None
        elif len(self.supermarkets) == 1:
            self.final_matches = products
        else:
            self.final_matches = self._get_matching_of_products(products)
            
    def _get_matching_of_products(self, products):
        
        result = []
        
        while products:
            
            product = products.pop(0)
            
            matchings_of_product = self._get_matchings_of_products_bfs([product], products)
            result.append(matchings_of_product)
            products = list(set(products) - set(matchings_of_product))
        
        
        i = 0
        
        print(result[:10])
        
        for match in result:
            if match and len(match) > 1:
                print([(prod.name, prod.supermarket.name) for prod in match])
                i += 1
            
            if i > 10:
                break
        else:
            print("Iteración: " + str(i))
        
        return result
    
    def _get_matchings_of_products_bfs(self, queue, products):
        
        result = []
        checked_supermarkets = set()
        
        while queue:
            product = queue.pop(0)
            result.append(product)
            checked_supermarkets.add(product.supermarket.name)
            for product_to_compare in products:
                
                if self._get_root_category(product.category).name != "Perfumería e Higiene" and self._get_root_category(product.category).name != "Limpieza y Hogar" and self._get_root_category(product_to_compare.category) == self._get_root_category(product.category) and product_to_compare.supermarket.name not in checked_supermarkets and product_to_compare not in result and self._is_match(product, product_to_compare):
                    print("Match para: ", product.name, " -> ", product_to_compare.name)
                    queue.append(product_to_compare)
                    
        return result
    
    def _is_match(self, product1, product2):
        
        if product1.supermarket == product2.supermarket or product1.brand != product2.brand or product1.brand is None and product2.brand is None:
            return False
        
        print(f"Comparando {product1.name}({product1.supermarket.name}) con {product2.name}({product2.supermarket.name})")
        
        
        if self._same_weight(product1.weight, product2.weight) is False:
            return False
        
        name_similarity = self._similarity_calculator(self.nlp(product1.name.strip()), self.nlp(product2.name.strip()), product1.brand)
        print(f"Similarity: {name_similarity}")
        if name_similarity > NAME_SIMILARITY_THRESHOLD:
            return True
        
        return False
    
    def _same_weight(self, weight1, weight2):
        
        if not weight1 or not weight2:
            return None

        if weight1 == weight2:
            return True
        
        parsed_weight1 = self._parse_weight_to_is(weight1)
        parsed_weight2 = self._parse_weight_to_is(weight2)
        
        if parsed_weight1 is None or parsed_weight2 is None:
            return None
        
        return parsed_weight1 == parsed_weight2
    
    @staticmethod
    def _parse_weight_to_is(weight):
        
        result = None
        weight = weight.lower()
        selected_unit_list = None
        
        for unit in DISTANCE_UNITS + VOLUME_UNITS + MASS_UNITS:
            if unit in weight:
                try:
                    weight = float(weight.replace(unit, "").strip())
                except ValueError:
                    break
                
                if unit in DISTANCE_UNITS:
                    selected_unit_list = DISTANCE_UNITS
                elif unit in VOLUME_UNITS:
                    selected_unit_list = VOLUME_UNITS
                elif unit in MASS_UNITS:
                    selected_unit_list = MASS_UNITS
                    
                index = selected_unit_list.index(unit)
                
                if index == 0:
                    result = weight/1000
                elif index == 1:
                    result = weight
                else:
                    parsing_factor = index-1
                    result = weight*10**parsing_factor
                break
            
        return result
    
    def _similarity_calculator(self, doc1, doc2, brand):
        
        nouns_set1 = set()
        adjectives_set1 = set()
        proper_nouns_set1 = set()
        others_set1 = set()
        nouns_set2 = set()
        adjectives_set2 = set()
        proper_nouns_set2 = set()
        others_set2 = set()
        
        brand = brand.name.lower() if brand else "" 
        
        for word in doc1.sentences[0].words:
            
            if word.upos == 'NOUN':
                nouns_set1.add(word.text.lower())
                
            elif word.upos == 'ADJ':
                adjectives_set1.add(word.text.lower())
                
            elif word.upos == 'PROPN':
                if word.text.lower() != brand:
                    proper_nouns_set1.add(word.text.lower())
                
            else:
                if word.upos == 'NUM' or word.upos == 'X':
                    others_set1.add(word.text.lower())
                
        for word in doc2.sentences[0].words:
            
            if word.upos == 'NOUN':
                nouns_set2.add(word.text.lower())
                
            elif word.upos == 'ADJ':
                adjectives_set2.add(word.text.lower())
                
            elif word.upos == 'PROPN':
                if word.text.lower() != brand:
                    proper_nouns_set2.add(word.text.lower())
                
            else:
                if word.upos == 'NUM' or word.upos == 'X':
                    others_set2.add(word.text.lower())
            
        coef_nouns = self.dice_coefficient(nouns_set1, nouns_set2)
        coef_adjectives = self.dice_coefficient(adjectives_set1, adjectives_set2)
        coef_propnouns = self.dice_coefficient(proper_nouns_set1, proper_nouns_set2)
        coef_other = self.dice_coefficient(others_set1, others_set2)
        
        mean = self._calculate_mean(coef_nouns, coef_adjectives, coef_propnouns, coef_other)
        
        return mean
    
    @staticmethod
    def _calculate_mean(coef_nouns, coef_adjectives, coef_propnouns, coef_other):
            
        return 0.4 * coef_nouns + 0.2 * coef_adjectives + 0.3 * coef_propnouns + 0.1 * coef_other
    
    @staticmethod
    def dice_coefficient(set1, set2):
        
        if len(set1) == 0 and len(set2) == 0:
            return 1.0
        elif len(set1) == 0 or len(set2) == 0:
            return 0.0
        else:
            return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))
    
    def _get_root_category(self, category, old_categories=None):
        if category in self.categories_mem:
            if old_categories:
                for old_category in old_categories:
                    self.categories_mem[old_category] = self.categories_mem[category]
            return self.categories_mem[category]

        old_categories = old_categories or []
        
        if category.parent:
            old_categories.append(category)
            category = self._get_root_category(category.parent, old_categories)
        
        for old_category in old_categories:
            self.categories_mem[old_category] = category
        
        return category
    
    def _stores_possible_matches(self):
        sqlite_products = self.classificator_api.get_products_scraped()
        products = self._parse_classificator_sqlite_products(sqlite_products)
        
        total_matches = 0
        
        while products:
            
            product = products.pop(0)
            
            for product_to_compare in products:
                if product.supermarket == product_to_compare.supermarket or product.category != product_to_compare.category or product.brand != product_to_compare.brand or not self._same_weight(product.weight, product_to_compare.weight):
                    continue
                total_matches += 1
                print(f"Posible matching {total_matches}")
                self.classificator_api.add_match(product, product_to_compare, None)
        
        print("Total matches: ", total_matches)
        
    def _stores_data(self, products):
        self.classificator_api.add_products_scraped(products)
        
    def _parse_classificator_sqlite_products(self, sqlite_products):
        return [ProductScraped(
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
                                            supermarket=str(product[19]),
                                            )
                                        for product in sqlite_products
                                    ]
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 6 ----------------------------
    
    # def _build_products(self):
    #     for match in self.final_matches:
    #         key_product = match[0]
    #         product, _ = Product.objects.get_or_create(
    #             name=key_product.name, 
    #             brand=key_product.brand, 
    #             image=key_product.image, 
    #             is_vegetarian=self._get_flag(match, "is_vegetarian"),
    #             is_gluten_free=self._get_flag(match, "is_gluten_free"),
    #             is_eco=self._get_flag(match, "is_eco"),
    #             is_freezed=self._get_flag(match, "is_freezed"),
    #             is_without_sugar=self._get_flag(match, "is_without_sugar"),
    #             is_without_lactose=self._get_flag(match, "is_without_lactose"),
    #             is_from_country=self._get_flag(match, "is_from_country"),
    #             category = self._get_leaf_category(match)
    #             )
    #         for product in match:
                
    #             # for pack in self.packs_scraped.filter(product_scraped=product):
    #             #     pack.product = product
    #             #     pack.save()
                
    #             price = Price.objects.create(
                    
    #             )
    
    @staticmethod
    def _get_flag(products, flag):
        for product in products:
            if product.__dict__[flag]:
                return True
            
        return False
    
    def _get_leaf_category(self, products):
        result = []
        for product in products:
            category_num_times = self._get_category_num_times(product.category)
            result.append((category_num_times, product.category))
        
        return max(result, key=lambda x: x[0])[1]
    
    def _get_category_num_times(self, category, result=0):
        if category.parent:
            return self._get_category_num_times(category.parent, result+1)
        
        return result
    
    # -----------------------------------------------------------------