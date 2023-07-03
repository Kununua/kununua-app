from unidecode import unidecode
import os

FILE_PATH = os.path.join('data', 'datasets', 'clean', 'brands.csv')

def clean_brands():
    print("Cleaning brands...")
    with open(FILE_PATH, 'r') as f:
        brands_csv = f.read()
    
    brands_list = brands_csv.split('\n')
    brands_list = list(set([_parse_brand(brand) for brand in brands_list]))
    os.remove(FILE_PATH)
    
    with open(FILE_PATH, 'w') as f:
        for brand in brands_list:
            if brands_list.index(brand) == len(brands_list) - 1:
                f.write(brand)
            else:
                f.write(f'{brand}\n')
    print("Brands cleaned successfully!")
    
def _parse_brand(brand):
    return unidecode(brand.lower().title().strip())

if __name__ == '__main__':
    clean_brands()