import requests, os
from tqdm import tqdm
from django.core.management.base import BaseCommand
from products.models import Product, Price


class Command(BaseCommand):
    help = 'Downloads the product images from the web'

    # https://www.supermercadoseljamon.com/documents/10180/892067/28001070_M.jpg

    def handle(self, *args, **options):
        
        products = Product.objects.all()
        packs = Price.objects.filter(amount__gt=1)
        
        download_pictures(products)
        download_pack_pictures(packs)
        
        remove_backgrounds(products)
        
        
      
# ---------------------------- PRIVATE FUCTIONS ----------------------------              

def download_pictures(products):
    
    print("1. Downloading images...")
        
    for product in tqdm(products):
    
        if "products" not in product.image.url:
            
            url = product.image
            file_name = normalize(product.name.replace(' ', '_').replace(",", "_").replace("/", "")) + normalize(product.price_set.first().weight.replace(' ', '_').replace(",", "_").replace("/", "")) + '.jpg'
    
            if picture_in_media(file_name):
                product.image = "products/images/%s" % (file_name)
                product.save()
            else:
                try:
                    try:
                        res = requests.get(url, stream = True, verify=True)
                    except requests.exceptions.SSLError:
                        res = requests.get(url, stream = True, verify=False)

                    if res.status_code == 200:
                        
                        product.image.save(file_name, res.raw, save=True)
                    
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                    print("Error")
                    product.image = "products/images/nodisponible.png"
                    product.save()
                    
def download_pack_pictures(packs):
    
    print("1. Downloading images...")
        
    for pack in tqdm(packs):
    
        if "products" not in pack.image.url:
            
            url = pack.image
            file_name = normalize(pack.product.name.replace(' ', '_').replace(",", "_").replace("/", "")) + normalize(pack.weight.replace(' ', '_').replace(",", "_").replace("/", "")) + f"-pack-{pack.amount}.jpg"
    
            if picture_in_media(file_name):
                pack.image = "products/images/%s" % (file_name)
                pack.save()
            else:
                try:
                    try:
                        res = requests.get(url, stream = True, verify=True)
                    except requests.exceptions.SSLError:
                        res = requests.get(url, stream = True, verify=False)

                    if res.status_code == 200:
                        
                        pack.image.save(file_name, res.raw, save=True)
                    
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                    print("Error")
                    pack.image = "products/images/nodisponible.png"
                    pack.save()

def remove_backgrounds(products):
    print("2. Removing backgrounds...")
    print("In future updates, this function will remove the background of the images.")

def picture_in_media(file_name):
    return os.path.exists("media/products/images/%s" % (file_name))

def normalize(s):
            replacements = (
                ('á', 'a'),
                ('é', 'e'),
                ('í', 'i'),
                ('ó', 'o'),
                ('ú', 'u'),
                ('ñ', 'n'),
            )
            
            for a, b in replacements:
                s = s.replace(a, b).replace(a.upper(), b.upper())
                
            return s