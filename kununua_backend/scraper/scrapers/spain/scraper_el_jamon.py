from bs4 import BeautifulSoup
from ...utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
from ...configuration_tools import ConfigurationTools
from products.models import Supermarket, Category
from ...models import ProductScraped
from location.models import Country
from ...utils.ProductShelf import ProductShelf
from tqdm import tqdm

supermarket = Supermarket(name="El Jamón", zipcode="41009", main_url="https://www.supermercadoseljamon.com/inicio", country=Country.objects.get(code='ESP'))

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)
 
	products = []
	category_selector = path.split(';')[-1].strip()
 
	while True:
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')
		category = soup.select(category_selector)[0].get_text().strip()
		common_parent = soup.select('.articulo')
		for item in common_parent:
			brand = item.select('.marca')[0].get_text().strip()
			multifield_1 = item.select('.nombre > a')[0]
			name, _ = tuple(multifield_1.get_text().strip().split(',') if len(multifield_1.get_text().strip().split(',')) == 2 else (multifield_1.get_text().strip(), None))
			name_link = multifield_1.get('href').strip()
			if item.select('.precio > span.tachado'):
				offer_price = float(item.select('.precio > span:nth-child(2)')[0].get_text().replace("€","").replace(",",".").strip())
				unit_price = item.select('.texto-porKilo')[0].get_text().strip()
				price = float(item.select('.precio > span.tachado')[0].get_text().replace("€","").replace(",",".").strip())
			else:
				offer_price = None
				unit_price = item.select('.texto-porKilo')[0].get_text().strip()
				price = float(item.select('.precio > span')[0].get_text().replace("€","").replace(",",".").strip())
			product_image = item.select('.imgwrap > img')[0].get('src').strip()
			is_from_country = True if item.find('img', alt='Andaluz') else False
			is_gluten_free = True if item.find('img', alt='Sin Gluten') else False
			is_freezed = True if item.find('img', alt='Congelado') else False
			is_vegan = True if item.find('img', alt='Vegano') else False
			is_eco = True if item.find('img', alt='Eco') else False
			is_without_sugar = True if item.find('img', alt='Sin Azucar') else False
			is_without_lactose = True if item.find('img', alt='Sin Lactosa') else False
			
			products.append(ProductScraped(name=name, price=price, unit_price=unit_price, brand=brand, offer_price=offer_price, image=product_image, is_from_country=is_from_country, is_gluten_free=is_gluten_free, is_freezed=is_freezed, is_vegetarian=is_vegan, is_eco=is_eco, is_without_sugar=is_without_sugar, is_without_lactose=is_without_lactose, url=name_link, supermarket=supermarket, category=Category(name=category)))
   
		# Finish pagination configuration in this section
		try:
			ConfigurationTools.run_pagination_eljamon(selenium_utils)
		except Exception:
			break
  
	return products

def scraper():
    
	print("Starting webdriver...")
	driver_options = webdriver.ChromeOptions()
	driver_options.headless = False
	driver = webdriver.Chrome(options=driver_options)
	selenium_utils = SeleniumUtils(timeout=10, driver=driver)
	
	driver.get('https://www.supermercadoseljamon.com/inicio')
	
	#Include the zipcode configuration in this section
	ConfigurationTools.zipcode_eljamon(selenium_utils)
	#-------------------------------------------------

	tree_paths = ['None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(1) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(2) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(3) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(4) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(5) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(6) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(7) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(8) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(9) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(10) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(11) > a.link-botcategoria > span'] 

	products = []
 
	print("Extracting data...")

	for path in tqdm(tree_paths): 
		products_to_add = extract_data('https://www.supermercadoseljamon.com/inicio', path, driver, selenium_utils)
		
		products += products_to_add

	driver.quit()

	shelve_util = ProductShelf('data/shelves/new-products-scraped')
	shelve_util.create_shelf(products)
