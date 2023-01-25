import requests, shutil
from tqdm import tqdm
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Downloads the product images from the web'

    # https://www.supermercadoseljamon.com/documents/10180/892067/28001070_M.jpg

    def handle(self, *args, **options):
        
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
        
        products = Product.objects.all()
        
        print("Downloading images...")
        
        for product in tqdm(products):
        
            if "products" not in product.image.url:
        
                url = product.image
                file_name = normalize(product.name.replace(' ', '_').replace(",", "_").replace("/", "")) + '_' + normalize(product.supermarket.name) + '.jpg'

                res = requests.get(url, stream = True)

                if res.status_code == 200:
                    
                    product.image.save(file_name, res.raw, save=True)
                    
                else:
                    print('Image Couldn\'t be retrieved')