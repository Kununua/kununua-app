from ...models import ProductScraped
from products.models import Supermarket, Category
from location.models import Country
from tqdm import tqdm
import time, requests

supermarket = Supermarket(name="Mercadona", zipcode="41009", main_url="https://www.mercadona.es", country=Country.objects.get(code='ESP'))

GET_ALL_CATEGORIES_URL = "https://tienda.mercadona.es/api/categories/?lang=es&wh=svq1"

def supermarket_in_db(supermarket, sqlite_api):
		supermarkets = sqlite_api.get_supermarkets()
		for supermarket_db in supermarkets:
			if supermarket_db[1] == supermarket.name and supermarket_db[2] == supermarket.zipcode and supermarket_db[3] == supermarket.main_url:
				return True
		return False

def get_products_from_category(category_id):
	
    request_url = f"https://tienda.mercadona.es/api/categories/{category_id}/?lang=es&wh=svq1"

    response = requests.get(request_url)

    if response.status_code == 200:

        products = []

        for subsubcategory in response.json()["categories"]:
            for product in subsubcategory["products"]:
                products.append(product)

        return products

    else:
        print(f"Error: {response}")
        raise Exception("Error getting products from category")
    
def get_product_details(product_id):
	
    request_url = f"https://tienda.mercadona.es/api/products/{product_id}/?lang=es&wh=svq1"

    response = requests.get(request_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response}")
        return {}
    
def map_product_to_model(product, category):
      
        if product["published"]:

            product_details = get_product_details(product["id"])

            name = product["display_name"]
            try:
                ean = product_details["ean"]
            except:
                print(product_details)
                ean = None
            price = float(product["price_instructions"]["unit_price"])
            
            if product["price_instructions"]["previous_unit_price"]:
                price = float(product["price_instructions"]["previous_unit_price"])
                offer_price = float(product["price_instructions"]["unit_price"])
            else:
                offer_price = None

            weight = str(product["price_instructions"]["unit_size"]) + product["price_instructions"]["reference_format"]
            
            try:
                amount = product["price_instructions"]["total_units"]
            except:
                amount = None
            image = product["thumbnail"]
            is_pack = product["price_instructions"]["is_pack"]
            product_url = product["share_url"]

            return ProductScraped(name=name, ean=ean, price=price, offer_price=offer_price, weight=weight, image=image, is_pack=is_pack, amount=amount, url=product_url, supermarket=supermarket, category=category)
        else:
            return None

def scraper(sqlite_api):

    # ----------------- SAVE SUPERMARKET IF NECESARY -----------------

    current_category_counter = int(sqlite_api.select_data("mercCache", "counter", None)[0][0])
    print(f"Current category counter: {current_category_counter}")

    if not supermarket_in_db(supermarket, sqlite_api):
        sql_supermarket = {"name": supermarket.name, "zipcode": supermarket.zipcode, "main_url": supermarket.main_url, "country": supermarket.country.code}
        sqlite_api._add_supermarket(sql_supermarket)
	
    # ----------------- CATEGORIES EXTRACTION -----------------

    categories_response = requests.get(GET_ALL_CATEGORIES_URL).json()

    global_categories = categories_response["results"]

    categories_to_extract = []

    for category in global_categories:
          for sub_category in category["categories"]:
              categories_to_extract.append(sub_category)

    # ----------------- PRODUCTS EXTRACTION ----------------- (implementar cache para extraccion de ean)

    for i in range(current_category_counter, len(categories_to_extract)):
        
        category = categories_to_extract[i]
          
        products_response = get_products_from_category(category["id"])

        print(f"Category: {category['name']} - Products: {len(products_response)}")

        products = []

        for product in products_response:

            product_parsed = map_product_to_model(product, category["name"])

            if product_parsed.ean == None:
                raise Exception(f"Product without EAN: {product_parsed.name}")

            if product_parsed:
                products.append(product_parsed)
        
        sqlite_api.add_products_scraped(products)
        sqlite_api.update_data("mercCache", "counter="+str(i + 1), "id=1")