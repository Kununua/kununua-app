import requests, os
from tqdm import tqdm
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Downloads the product images from the web'

    # https://www.supermercadoseljamon.com/documents/10180/892067/28001070_M.jpg

    def handle(self, *args, **options):
        
        products = Product.objects.all()
        
        download_pictures(products)
        
        remove_backgrounds(products)
        
        
      
# ---------------------------- PRIVATE FUCTIONS ----------------------------              

def download_pictures(products):
    
    print("1. Downloading images...")
        
    for product in tqdm(products):
    
        if "products" not in product.image.url:
            
            url = product.image
            file_name = normalize(product.name.replace(' ', '_').replace(",", "_").replace("/", "")) + '.jpg'
    
            if picture_in_media(file_name):
                product.image = "products/images/%s" % (file_name)
                product.save()
            else:
                try:

                    res = requests.get(url, stream = True, verify=True)

                    if res.status_code == 200:
                        
                        product.image.save(file_name, res.raw, save=True)
                    
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                    print("Error")
                    product.image = "products/images/nodisponible.png"
                    product.save()

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