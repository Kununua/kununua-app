from ...models import ProductScraped
from products.models import Supermarket, Category
from location.models import Country
from tqdm import tqdm
import time, requests

supermarket = Supermarket(name="Carrefour", zipcode="41009", main_url="https://www.carrefour.es", country=Country.objects.get(code='ESP'))

CARREFOUR_API_LIMIT = 1001

CATEGORIES_IDS = {
    "productos+frescos" : "category_ids_2%3Acat20002",
    "la+despensa": "category_ids_2%3Acat20001",
    "congelados": "category_ids_2%3Acat21449123",
    "bebidas": "category_ids_2%3Acat20003",
    "limpieza+y+hogar": "category_ids_2%3Acat20005",
    "perfumería+e+higiene": "category_ids_2%3Acat20004",
    "bebé": "category_ids_2%3Acat20006",
    "mascotas": "category_ids_2%3Acat20007",
    "parafarmacia": "category_ids_2%3Acat20008"
}

CATEGORIES_TO_EXTRACT = {
    "carnicería": "productos+frescos",
    "pescadería": "productos+frescos",
    "frutas": "productos+frescos",
    "verduras+y+hortalizas": "productos+frescos",
    "panadería+tradicional": "productos+frescos",
    "charcutería": "productos+frescos",
    "quesos": "productos+frescos",
    "platos+preparados+cocinados": "productos+frescos",
    "alimentación": "la+despensa",
    "lácteos": "la+despensa",
    "yogures+y+postres": "la+despensa",
    "dulce+y+desayuno": "la+despensa",
    "panadería%2C+bollería+y+pastelería": "la+despensa",
    "conservas%2C+sopas+y+precocinados": "la+despensa",
    "aperitivos": "la+despensa",
    "huevos": "la+despensa",
    "rebozados+y+platos+preparados": "congelados",
    "pizzas+congeladas": "congelados",
    "verduras+congeladas": "congelados",
    "salteados+congelados": "congelados",
    "helados": "congelados",
    "mariscos+congelados": "congelados",
    "pescados+congelados": "congelados",
    "gulas+y+surimis+congelados": "congelados",
    "pulpo%2C+calamar+y+sepia+congelados": "congelados",
    "refrescos": "bebidas",
    "cerveza": "bebidas",
    "aguas+y+zumos": "bebidas",
    "alcoholes": "bebidas",
    "vinos": "bebidas",
    "cava+y+champagne": "bebidas",
    "licores+y+cremas": "bebidas",
    "sidra": "bebidas",
    "cuidado+de+la+ropa": "limpieza+y+hogar",
    "papel+y+celulosa": "limpieza+y+hogar",
    "productos+para+cocina": "limpieza+y+hogar",
    "productos+para+baño": "limpieza+y+hogar",
    "productos+para+toda+la+casa": "limpieza+y+hogar",
    "utensilios+de+limpieza": "limpieza+y+hogar",
    "conservación+de+alimentos": "limpieza+y+hogar",
    "ambientadores": "limpieza+y+hogar",
    "calzado": "limpieza+y+hogar",
    "menaje": "limpieza+y+hogar",
    "papelería": "limpieza+y+hogar",
    "bazar": "limpieza+y+hogar",
    "baño+e+higiene+corporal": "perfumería+e+higiene",
    "cabello": "perfumería+e+higiene",
    "cuidado+y+protección+corporal": "perfumería+e+higiene",
    "boca+y+sonrisa": "perfumería+e+higiene",
    "higiene+íntima": "perfumería+e+higiene",
    "depilación+y+afeitado": "perfumería+e+higiene",
    "cosmética": "perfumería+e+higiene",
    "bienestar+sexual": "perfumería+e+higiene",
    "pañales+y+toallitas": "bebé",
    "alimentación+infantil": "bebé",
    "perfumería+e+higiene": "bebé",
    "embarazo+y+lactancia": "bebé",
    "puericultura": "bebé",
    "perros": "mascotas",
    "gatos": "mascotas",
    "conejos+y+roedores": "mascotas",
    "pájaros": "mascotas",
    "peces+y+tortugas": "mascotas",
    "bebé": "parafarmacia",
    "higiene+bucal": "parafarmacia",
    "botiquín": "parafarmacia",
    "cuidado+corporal": "parafarmacia",
    "cuidado+e+higiene+facial": "parafarmacia",
    "cabello": "parafarmacia",
    "cuidado+de+manos+y+pies": "parafarmacia",
    "nutrición+y+dietética": "parafarmacia",
}

def supermarket_in_db(supermarket, sqlite_api):
		supermarkets = sqlite_api.get_supermarkets()
		for supermarket_db in supermarkets:
			if supermarket_db[1] == supermarket.name and supermarket_db[2] == supermarket.zipcode and supermarket_db[3] == supermarket.main_url:
				return True
		return False

def get_products_from_category(category, category_parent):
	
    request_url = f"https://www.carrefour.es/search-api/query/v1/search?query={category}&lang=es&catalog=food&rows=50000&start=0&origin=linked&f.op=OR&filter={CATEGORIES_IDS[category_parent]}"

    headers = {
         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
         "Cookie": "session_id=2R3UX04bO3hWizT5AtopfqEl2EG; kppid_managed=kppid_Pm5rEjRy; __gads=ID=5ff56b8804df7f71:T=1686439637:RT=1686480018:S=ALNI_MY27dSQbYBLl-cMUnB709rIsio3ew; __gpi=UID=00000c2e9cf4dbed:T=1686439637:RT=1686480018:S=ALNI_Mb8ARDkPpj40Ebjtl8Ff6UqvCgOlQ; _fbp=fb.1.1686416498148.1484110189; _ga=GA1.2.2035753193.1686416494; _ga_KPXW54NX57=GS1.1.1686478294.3.1.1686480018.51.0.0; _gid=GA1.2.726409580.1686416497; _pin_unauth=dWlkPU1UTmhaREF3WXpVdE5qTTBNaTAwTVdZekxXRTJOR010T0dSaVptVXlaREl6TUdFMQ; _gcl_au=1.1.2028865662.1686416497; _cs_id=0c91699b-b38f-a0e4-9cb3-cbf117191275.1686439636.2.1686480015.1686478294.1.1720603636574; _cs_s=14.0.0.1686481815723; cto_bundle=A50NTF8ycjFzViUyRnglMkZscFl4SzlLcWF0TmJBd2ZRVjkwQlgzSHF0ZDY0NkxXUWxQWUhrdm9qNXpYcWp1U1lVQkttQjlEVHh1SE01TlNQYnowYkRpTDNRZiUyRmw3NGJ2cEZ5b2VjUFlLeldUaTFHOVlYbDN4WU83UkxwZmRlOEJuVkRKUTVDRA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; _uetsid=5b7b3200084011eeab5503a848662cef; _uetvid=5b7b48b0084011eea0acb9887f9e93e2; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jun+11+2023+12%3A40%3A14+GMT%2B0200+(hora+de+verano+de+Europa+central)&version=202302.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0097%3A1%2CC0001%3A1%2CC0022%3A1%2CC0007%3A1%2CC0166%3A1%2CC0096%3A1%2CC0021%3A1%2CC0052%3A1%2CC0063%3A1%2CC0174%3A1%2CC0081%3A1%2CC0101%3A1%2CC0051%3A1%2CC0023%3A1%2CC0025%3A1%2CC0032%3A1%2CC0033%3A1%2CC0036%3A1%2CC0038%3A1%2CC0039%3A1%2CC0041%3A1%2CC0056%3A1%2CC0082%3A1%2CC0128%3A1%2CC0135%3A1%2CC0005%3A1%2CC0180%3A1%2CC0084%3A1%2CC0167%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; incap_ses_1311_769673=QRSZAbQdJzPJVFINZJwxEgWfhWQAAAAAt2u4tFESRXD9vUvtI41gRQ==; nlbi_769673=j++yKuSYzBshu7NiIk/qZQAAAABPnBLemeIfwTNk9bLuLWr4; incap_ses_1556_769673=/ZO5SLmpp3Zu9QRkHAaYFdydhWQAAAAA977zZz8Pw96Uk+XmalN3ug==; Wizard=true; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22a34hyrA1lFltDDDuRamM%22%7D; t2s-p=54726e3c-c3ed-42ba-a7c7-e95aecf55df3; incap_ses_1311_258278=ThS6BR49khLlflENZJwxEtSdhWQAAAAASsCn5KbaqIg7neS1Bnjq9Q==; nlbi_258278_1838428=dBGRSbWzQRnZCZmMpd9X5AAAAAB1ChVX1HyITO4VU5Yh+qVO; salepoint=005704||28019|A_DOMICILIO|0; _cs_c=1; t2s-analytics=54726e3c-c3ed-42ba-a7c7-e95aecf55df3; OneTrustGroupsConsent-ES=,C0097,C0001,C0022,C0007,C0166,C0096,C0021,C0052,C0063,C0174,C0081,C0101,C0051,C0023,C0025,C0032,C0033,C0036,C0038,C0039,C0041,C0056,C0082,C0128,C0135,C0005,C0180,C0084,C0167,C0004,; _tt_enable_cookie=1; _ttp=2aaei27jmQkzqZVOb1dHy2BhBXV; OptanonAlertBoxClosed=2023-06-10T17:01:37.307Z; visid_incap_769673=4ssp7N9tQ7apYrdkmaXs62yshGQAAAAAQUIPAAAAAACszFzRgDw9RWXGeAdbBIYy; visid_incap_258278=RTp+DDwWSROmfAKYfDfINGyshGQAAAAAQUIPAAAAAAAraTzrMywSSaq8u94j5+6N"
    }

    response = requests.get(request_url, headers=headers)

    if response.status_code == 200:
        
        try:
            products = response.json()["content"]["docs"]
            num_found = response.json()["content"]["numFound"]

            while len(products) < num_found and len(products) < CARREFOUR_API_LIMIT:
                request_url = f"https://www.carrefour.es/search-api/query/v1/search?query={category}&lang=es&catalog=food&rows=50000&start={len(products)}&origin=linked&f.op=OR&filter={CATEGORIES_IDS[category_parent]}"
                response = requests.get(request_url, headers=headers)

                if response.status_code == 200:

                    products += response.json()["content"]["docs"]
                
                else:
                    print(f"Error: {response}")
                    raise Exception("Error getting products from category")

            print(f"Found {len(products)} products in category {category}")

            return products
        
        except Exception as e:
            print(e)
            print(f"Error: {response}")
            raise Exception("Error getting products from category")

    else:
        print(f"Error: {response}")
        raise Exception("Error getting products from category")
    
def map_product_to_model(product, category):
      
    try:
        name = product["display_name"]
        ean = product["ean13"]

        if product["list_price"] != product["active_price"]:
            price = float(product["list_price"])
            offer_price = float(product["active_price"])
        else:
            price = float(product["active_price"])
            offer_price = None

        try:
            brand = product["brand"]
        except:
            brand = None

        unit_price = product["price_per_unit_text"]
        
        if ' pack ' in name:
            is_pack = True
            try:
                pack_info = name.split(' pack ')[1].strip().split(' ')
                if pack_info[0] == 'de':
                    if 'x' in pack_info[1]:
                        amount = int(pack_info[1].split('x')[0])
                    else: 
                        amount = int(pack_info[1])
                else:
                    if 'x' in pack_info[0]:
                        amount = int(pack_info[0].split('x')[0])
                    else: 
                        amount = int(pack_info[0])
                    
                name = name.split(' pack ')[0].strip()
                
            except Exception:
                amount = None
        else:
            is_pack = False
            amount = None
        
        image = product["image_path"]
        product_url = supermarket.main_url + str(product["url"])

        return ProductScraped(name=name, ean=ean, price=price, brand=brand, offer_price=offer_price, unit_price=unit_price, image=image, is_pack=is_pack, amount=amount, url=product_url, supermarket=supermarket, category=category)
    except Exception as e:
        print(e)
        print(f"Error mapping product {product['display_name']}")
        raise Exception("Error mapping product")
        

def scraper(sqlite_api):

    # ----------------- SAVE SUPERMARKET IF NECESARY -----------------

    if not supermarket_in_db(supermarket, sqlite_api):
        sql_supermarket = {"name": supermarket.name, "zipcode": supermarket.zipcode, "main_url": supermarket.main_url, "country": supermarket.country.code}
        sqlite_api._add_supermarket(sql_supermarket)
	
    products = []

    for category, category_parent in tqdm(CATEGORIES_TO_EXTRACT.items()):
          
        products_response = get_products_from_category(category, category_parent)

        for product in products_response:

            product_parsed = map_product_to_model(product, category)

            if product_parsed.ean == None:
                raise Exception(f"Product without EAN: {product_parsed.name}")

            if product_parsed:
                products.append(product_parsed)

    
    sqlite_api.add_products_scraped(products)