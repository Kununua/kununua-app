import json, stanza, math, re
from pathlib import Path
from products.models import Product, Brand, Supermarket, Category, Price
from location.models import Country
from data.functions.get_brands_list import get_brands_list
from scraper.models import ProductScraped, PackScraped
from scraper.utils.SimilarityCalculator import SimilarityCalculator
from data.similarities_threshold import THRESHOLDS, NAME_SIMILARITY_THRESHOLD
from scraper.utils.ScraperSQLiteAPI import ScraperSQLiteAPI
from scraper.utils.ClassificatorSQLiteAPI import ClassificatorSQLiteAPI
from unidecode import unidecode

DISTANCE_UNITS = ["km", "m", "dm", "cm", "mm"]
VOLUME_UNITS = ["kl", "l", "dl", "cl", "ml"]
MASS_UNITS = ["kg", "g", "dg", "cg", "mg"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", "."]
NO_IMAGE_CARREFOUR = "data:image/jpeg;base64,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"
PACK_SIMILARITY_THRESHOLD = 0.8

UNIT_TRANSLATIONS = {
    "km": "km",
    "m": "m",
    "dm": "dm",
    "cm": "cm",
    "mm": "mm",
    "kl": "kl",
    "l": "l",
    "dl": "dl",
    "cl": "cl",
    "ml": "ml",
    "kg": "kg",
    "g": "g",
    "dg": "dg",
    "cg": "cg",
    "mg": "mg",
    'gr': 'g',
    'grs': 'g',
    'gramo': 'g',
    'gramos': 'g',
    'kilo': 'kg',
    'kilogramo': 'kg',
    'kilogramos': 'kg',
    'litro': 'l',
    'litros': 'l',
    'mililitro': 'ml',
    'mililitros': 'ml',
    'centilitro': 'cl',
    'centilitros': 'cl',
    'kgs': 'kg',
    'kilos': 'kg',
    'metros': 'm',
    'metro': 'm',
    'centimetros': 'cm',
    'centimetro': 'cm',
    'milimetros': 'mm',
    'milimetro': 'mm',
    'centímetros': 'cm',
    'centímetro': 'cm',
    'milímetros': 'mm',
    'milímetro': 'mm',
}



class MatchingUtil(object):
    def __init__(self, sqlite_products, sqlite_packs):
        self.sqlite_products = sqlite_products
        self.sqlite_packs = sqlite_packs
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
        print("Phase 2: Parsing sqlite result to packs objects...")
        self._parse_sqlite_packs(self.sqlite_packs)
        print("Phase 3: Performing brands matching...")
        self._brands_matching()
        print("Phase 4: Performing weight unification...")
        self._weight_unification()
        print("Phase 5: Performing packs matching...")
        self._packs_matching()
        print("Phase 6: Performing categories matching...")
        self._categories_matching()
        print("Phase 7: Performing products matching...")
        self._non_semanthic_products_matching()
        #self._products_matching()
        print("Phase 8: Translating and injecting into postgres...")
        self._build_products()
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
        print("Phase 5: Performing weight unification...")
        self._weight_unification()
        print("Phase 6: Storing products in new db...")
        self._stores_data(self.products_scraped)
        print("Phase 7: Storing possible matches in new db...")
        self._stores_possible_matches()
        print("Done!")
        
    # ------------------------------- PRIVATE FUNCTIONS -------------------------------
    
    # ---------------------------- PHASE 0 ----------------------------
    
    def _save_supermarkets(self):
        
        API = ScraperSQLiteAPI("scrapers_api.db")
        
        supermarkets = API.get_supermarkets(condition="supermarkets.country = countries.id")
        
        for supermarket in supermarkets:
            pg_supermarket, _ = Supermarket.objects.get_or_create(name=supermarket[1], zipcode=supermarket[2], main_url=supermarket[3], country=Country.objects.get(code=supermarket[8]), logo=f"supermarkets/logos/logo-{supermarket[1].lower()}.png", banner=f"supermarkets/banners/banner-{supermarket[1].lower()}.png")
            self.supermarkets.append(pg_supermarket)
            self.supermarkets_mapping[supermarket[0]] = pg_supermarket.pk
            
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 1 ----------------------------
    
    def _parse_sqlite_products(self, sqlite_products):
        
        self.products_scraped =  [ProductScraped(
                                            pseudo_id = int(product[0]),
                                            name=str(product[1]),
                                            ean=str(product[2]),
                                            price=float(product[3]),
                                            unit_price=str(product[4]) if product[4] else None,
                                            weight=str(product[5]) if product[5] else None,
                                            brand=str(product[6]) if product[6] else None,
                                            amount=int(product[7]) if product[7] else None,
                                            image=str(product[8]),
                                            offer_price=float(product[9]) if product[9] else None,
                                            is_vegetarian=bool(product[10]),
                                            is_gluten_free=bool(product[11]),
                                            is_freezed=bool(product[12]),
                                            is_from_country=bool(product[13]),
                                            is_eco=bool(product[14]),
                                            is_without_sugar=bool(product[15]),
                                            is_without_lactose=bool(product[16]),
                                            url=str(product[17]) if product[17] else None,
                                            is_pack=bool(product[18]),
                                            category=str(product[19]),
                                            supermarket=Supermarket.objects.get(pk=self.supermarkets_mapping[int(product[20])]),
                                            )
                                        for product in sqlite_products
                                    ]
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 2 ----------------------------
    
    def _parse_sqlite_packs(self, sqlite_packs):
        self.packs_scraped = [PackScraped(
                                name=str(pack[1]),
                                pack_ean=str(pack[2]),
                                amount=int(pack[3]),
                                price=float(pack[4]),
                                offer_price=float(pack[5]) if pack[5] else None,
                                weight=str(pack[6]) if pack[6] else None,
                                image=str(pack[7]),
                                url=str(pack[8]) if pack[8] else None,
                                product_scraped= next((product for product in self.products_scraped if product.pseudo_id == int(pack[9])), None),
                                )
                              
                                for pack in sqlite_packs
                            ]
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 3 ----------------------------
    
    def _brands_matching(self):
        """
        input: list of ProductScraped with ProductScraped.brand being None or a string
        output: list of ProductScraped with ProductScraped.brand being a Brand object or None
        """
        
        result = []
        
        for product in self.products_scraped:
            if product.brand:
                brands_list = Brand.objects.all().values_list('id', 'name')
                brands_list = [(id, self._unidecode_brand(brand_name)) for id, brand_name in brands_list]
                brand_id = self.get_brand_id(self._unidecode_brand(product.brand), brands_list)
                
                if brand_id:
                    brand = Brand.objects.get(pk=brand_id)
                else:
                    brand, new = Brand.objects.get_or_create(name__iexact=self._parse_brand(product.brand), defaults={'name': self._parse_brand(product.brand)})
                    if new:
                        with open('data/datasets/clean/brands.csv', 'a') as f:
                            f.write(f"\n{self._unidecode_brand(product.brand)}")
                            
                if self._parse_brand(product.brand) != brand.name and brand.name == self._unidecode_brand(product.brand):
                    brand.name = self._parse_brand(product.brand)
                    brand.save()
                
                product.brand = brand
                result.append(product) 
            else:
                brands = get_brands_list("data/datasets/clean/brands.csv")            
                for brand in brands:
                    if brand.lower() in unidecode(product.name.lower()):
                        brands_list = Brand.objects.all().values_list('id', 'name')
                        brands_list = [(id, self._unidecode_brand(brand_name)) for id, brand_name in brands_list]
                        brand_parsed = product.name[unidecode(product.name.lower()).index(brand.lower()):unidecode(product.name.lower()).index(brand.lower())+len(brand)]
                        brand_id = self.get_brand_id(brand, brands_list)
                        
                        if brand_id:
                            pg_brand = Brand.objects.get(pk=brand_id)
                        else:
                            pg_brand, new = Brand.objects.get_or_create(name__iexact=self._parse_brand(brand_parsed), defaults={'name': self._parse_brand(brand_parsed)})
                            if new:
                                with open('data/datasets/clean/brands.csv', 'a') as f:
                                    f.write(f"\n{self._unidecode_brand(pg_brand.name)}")
                                    
                        if self._parse_brand(brand_parsed) != pg_brand.name and pg_brand.name == brand:
                            pg_brand.name = self._parse_brand(brand_parsed)
                            pg_brand.save()
                              
                        product.brand = pg_brand
                        result.append(product)
                        break
                else:
                    result.append(product)
                    
        self.products_scraped = result

    @staticmethod
    def _parse_brand(brand):
        return brand.lower().title().strip()

    def _unidecode_brand(self, brand):
        return unidecode(self._parse_brand(brand))
    
    @staticmethod
    def get_brand_id(brand, brands_list):
        for id, brand_name in brands_list:
            if brand_name == brand:
                return id
        return None
     
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 4 ----------------------------
    
    def _weight_unification(self):
        
        for product in self.products_scraped:
            if product.weight:
                product.weight = product.weight.lower()
            if not product.weight and product.unit_price or product.supermarket.name == "Carrefour":
                product = self._unify_weight(product)
            elif product.weight and not product.unit_price:
                product = self._unify_unit_price(product)
        
    def _unify_weight(self, product):
        
        price = float(product.price)
        unit_price = product.unit_price
        weight_unit = unit_price.split("/")[1].strip()
        weight_unit_aux_value = re.sub('[a-z]+', '', weight_unit.lower())
        round_to = 1 if "ud" not in weight_unit and "unidad" not in weight_unit else 0
        unit_price_value = float(unit_price.split("/")[0].replace(".", "").replace(",", ".").replace("€", "").strip())
        
        try:
            weight_value = price/unit_price_value
        except ZeroDivisionError:
            product.unit_price = f"{price} €/ud"
            product.weight = "1ud"
            return product
        
        if weight_unit_aux_value:
            weight_value = str(weight_value * float(weight_unit_aux_value))
        else:
            weight_value = str(weight_value)
        
        try:
            weight_unit = UNIT_TRANSLATIONS[re.sub('\d+|\.', '', weight_unit.lower()).strip()]
        
            if weight_value.startswith("0."):
                
                weight_value_float = float(weight_value)
                
                index = self.get_unit_family(weight_unit).index(weight_unit)
                
                if index == 0:
                    weight_value_float = weight_value_float*1000
                elif index > 1:
                    parsing_factor = index-1
                    weight_value_float = weight_value_float/(10**parsing_factor)
                
                weight = str(round(weight_value_float, round_to)) + self.get_unit_family(weight_unit)[1]
            
            elif "." in weight_value:
                weight = str(round(float(weight_value), round_to)) + weight_unit
            else:
                weight = str(round(float(weight_value), round_to)) + weight_unit
            
            product.weight = weight
            
        except KeyError:
            product.weight = weight_value + weight_unit
            
        return product
    
    def _unify_unit_price(self, product):
        
        price = product.price
        weight = product.weight
        try:
            weight_unit = UNIT_TRANSLATIONS[re.sub('\d+|\.', '', weight.lower()).strip()]
        except KeyError:
            product.unit_price = f"{price} €/ud"
            product.weight = "1ud"
            return product
        weight_value = float(re.sub('[a-z]+', '', weight.lower()))
        
        selected_unit_family = self.get_unit_family(weight_unit)
        
        unit_price_value = price/weight_value
        
        if weight_unit in selected_unit_family[0] and math.floor(unit_price_value) > 100:
            
            weight_unit = selected_unit_family[1]
            unit_price_value = unit_price_value/1000
            
        elif weight_unit in selected_unit_family[1] and float('%.2f'%unit_price_value) == 0 :
            
            weight_unit = selected_unit_family[0]
            unit_price_value = unit_price_value*1000
            
        product.unit_price = str(unit_price_value) + " €/" + weight_unit
        
        return product
     
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 5 ----------------------------
    
    def _packs_matching(self):
        
        products_to_return = []
        packs_to_return = []
        
        for supermarket in self.supermarkets:
            
            products_to_add = []
            packs_to_add = []
            
            supermarket_products = [product for product in self.products_scraped if product.supermarket.name == supermarket.name and product.supermarket.zipcode == supermarket.zipcode]
            
            for product in supermarket_products:
                
                if product.is_pack:
                    product_of_pack_id = self._search_product_of_pack(product, supermarket_products)
                    
                    if product_of_pack_id is not None:
                        
                        try:
                            pack_amount = int(product.amount)
                        except Exception:
                            pack_amount = 1

                        try:
                            pack_weight = product.weight
                        except Exception:
                            print(product)
                            pack_weight = None
                            raise Exception("Pack weight is None")
                        
                        packs_to_add.append(PackScraped(product_scraped=product_of_pack_id, amount=pack_amount, price=product.price, weight=pack_weight, image=product.image, url=product.url))
                        continue
                
                products_to_add.append(product)
            
            products_to_return += products_to_add
            packs_to_return += packs_to_add

        self.products_scraped = products_to_return
        self.packs_scraped = packs_to_return
        
    def _search_product_of_pack(self, product, supermarket_products):
        
        match = None
        highest_similarity = 0
        
        # print(self.packs_scraped)
        
        for pack in self.packs_scraped:
            
            # print(product)
            # print(pack)
            
            if product.ean == pack.pack_ean:
                print(f"Pack matcheado mediante ean")
                return pack.product_scraped
        
        for product_to_compare in supermarket_products:
            
            similarity_coef = self.similarity.compute_string_similarity(product_to_compare.name, product.name)
            try:
                if product_to_compare.category == product.category and product_to_compare.supermarket.name == product.supermarket.name and product_to_compare.is_pack == False and similarity_coef > highest_similarity: #and product_to_compare.weight in product.weight:
                    highest_similarity = similarity_coef
                    match = product_to_compare
            except Exception:
                print(f"Error en la comparación de productos con el producto {product} y el producto a comparar {product_to_compare}")

        if match is None or highest_similarity < PACK_SIMILARITY_THRESHOLD:
            return None
        else:
            return match
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 6 ----------------------------
    
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
            image = f'categories/images/{category_splitted[i].lower().strip().replace(" ", "_")}.png'
            if i > 0:
                result, _ = Category.objects.get_or_create(name=category_splitted[i].strip(), parent=Category.objects.get(name=category_splitted[i-1].strip()), image=image)
            else:
                result, _ = Category.objects.get_or_create(name=category_splitted[i].strip(), image=image)
                
        return result
        
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 7 ----------------------------
    
    def _non_semanthic_products_matching(self):
        
        products = self.products_scraped
        products_aux = []
        result = []
        total_matches = 0
        
        while products:
            product = products.pop(0)
            similar_products = [product]
            products_aux.append(product)
            already_removed = False
                
            for product_to_compare in products:
                if product_to_compare.ean == product.ean:
                    similar_products.append(product_to_compare)
                    total_matches += 1
                    if not already_removed:
                        products_aux.pop()
                        already_removed = True
            
            products = [product for product in products if product not in similar_products]
            if len(similar_products) > 1:
                result.append(similar_products)

        print(products_aux[:10])

        while products_aux:
            
            product = products_aux.pop(0)
            similar_products = [product]
                
            for product_to_compare in products_aux:
                if product.supermarket == product_to_compare.supermarket or self._get_root_category(product.category) != self._get_root_category(product_to_compare.category) or product.brand != product_to_compare.brand or not self._same_weight(product.weight, product_to_compare.weight):
                    continue
                
                total_matches += 1
                similar_products.append(product_to_compare)
            
            products_aux = [product for product in products_aux if product not in similar_products]
            result.append(similar_products)
            
        print(f"Total matchings: {total_matches}")
        
        self.final_matches = result
    
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
        
        return (parsed_weight1 == parsed_weight2 + 1 or 
                parsed_weight1 == parsed_weight2 - 1 or 
                parsed_weight1 + 1 == parsed_weight2 or 
                parsed_weight1 - 1 == parsed_weight2 or 
                parsed_weight1 == parsed_weight2)
    
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
                                            ean=str(product[2]),
                                            price=float(product[3]),
                                            unit_price=str(product[4]) if product[4] else None,
                                            weight=str(product[5]) if product[5] else None,
                                            brand=str(product[6]) if product[6] else None,
                                            amount=int(product[7]) if product[7] else None,
                                            image=str(product[8]),
                                            offer_price=float(product[9]) if product[9] else None,
                                            is_vegetarian=bool(product[10]),
                                            is_gluten_free=bool(product[11]),
                                            is_freezed=bool(product[12]),
                                            is_from_country=bool(product[13]),
                                            is_eco=bool(product[14]),
                                            is_without_sugar=bool(product[15]),
                                            is_without_lactose=bool(product[16]),
                                            url=str(product[17]) if product[17] else None,
                                            is_pack=bool(product[18]),
                                            category=str(product[19]),
                                            supermarket=str(product[20]),
                                            )
                                        for product in sqlite_products
                                    ]
    
    # -----------------------------------------------------------------
    # ---------------------------- PHASE 8 ----------------------------
    
    def _build_products(self):
        
        for match in self.final_matches:
            key_product = match[0]
            try:
                product, _ = Product.objects.get_or_create(
                    name=key_product.name, 
                    brand=key_product.brand, 
                    image=key_product.image, 
                    is_vegetarian=self._get_flag(match, "is_vegetarian"),
                    is_gluten_free=self._get_flag(match, "is_gluten_free"),
                    is_eco=self._get_flag(match, "is_eco"),
                    is_freezed=self._get_flag(match, "is_freezed"),
                    is_without_sugar=self._get_flag(match, "is_without_sugar"),
                    is_without_lactose=self._get_flag(match, "is_without_lactose"),
                    is_from_country=self._get_flag(match, "is_from_country"),
                    category = self._get_leaf_category(match)
                )
                
                
                for other_product in match:
                    for pack in filter(lambda p: p.product_scraped.pseudo_id == other_product.pseudo_id, self.packs_scraped):
                        
                        pack_price, _ = Price.objects.get_or_create(
                            price = pack.price,
                            offer_price = pack.offer_price,
                            weight = pack.weight,
                            amount = pack.amount,
                            url = pack.url,
                            supermarket = pack.product_scraped.supermarket,
                            product = product,
                            image = pack.image
                        )
                    
                    other_product_price, _ = Price.objects.get_or_create(
                        price = other_product.price,
                        offer_price = other_product.offer_price,
                        weight = other_product.weight,
                        amount = 1 if other_product.offer_price else None,
                        url = other_product.url,
                        supermarket = other_product.supermarket,
                        product = product,
                        image = None
                    )
                    
            except Exception as e:
                print(e)
                print(key_product.name)
                break
    
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
    
    @staticmethod
    def get_unit_family(unit):
        if unit in DISTANCE_UNITS:
            return DISTANCE_UNITS
        elif unit in VOLUME_UNITS:
            return VOLUME_UNITS
        elif unit in MASS_UNITS:
            return MASS_UNITS
        else:
            return None
        
    @staticmethod
    def _parse_weight_to_is(weight, to_kilo_units=False):
        
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
                
                if not to_kilo_units:
                    if index == 0:
                        result = weight*1000
                    elif index == 1:
                        result = weight
                    else:
                        parsing_factor = index-1
                        result = weight/10**parsing_factor
                    break
                else:
                    if index == 0:
                        result = weight
                    elif index == 1:
                        result = weight/1000
                    else:
                        parsing_factor = index-1
                        result = weight/10**(parsing_factor+3)
                    break
            
        return result
    
    @staticmethod
    def _get_flag(products, flag):
        for product in products:
            if product.__dict__[flag]:
                return True
            
        return False