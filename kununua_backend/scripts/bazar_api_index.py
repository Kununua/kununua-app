from django.conf import settings
from whoosh import fields, index
import requests

PRODUCT_SCHEMA = fields.Schema(id=fields.ID(stored=False, unique=True), ean=fields.TEXT(stored=True),
                               name=fields.TEXT(stored=False), image=fields.TEXT(stored=True))
API_LIMIT = 100
API_URL = f'https://api.bazaarvoice.com/data/products.json?passkey=caUNHRYNaaEpio9tsasDler7d1kTrqmaNQQzskkyRX6mQ&locale=es_ES&allowMissing=true&apiVersion=5.4&limit={API_LIMIT}'
      
def _new_product(id, name, ean, image):
    ix = index.open_dir(settings.WHOOSH_INDEX, schema=PRODUCT_SCHEMA)
    writer = ix.writer() 
    writer.add_document(id=id, name=name, ean=ean, image=image)
    writer.commit()

def _get_products(offset):
    products = requests.get(f"{API_URL}&offset={offset}").json()["Results"]
    _create_products(products)

def _create_products(products):
    for product in products:
        if product["EANs"]:
            _new_product(product["Id"], product["Name"], product["EANs"][0], product["ImageUrl"])
            
def main():
    products = requests.get(f"{API_URL}&offset=0").json()
    total_offset = round(products["TotalResults"]/API_LIMIT)
    products = products["Results"]
    _create_products(products)
    
    for i in range(1, total_offset):
        _get_products(i)
            
if __name__ == "__main__":
    main()