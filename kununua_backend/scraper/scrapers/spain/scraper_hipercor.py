from bs4 import BeautifulSoup
from ...utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
import undetected_chromedriver as uc
from ...utils.ConfigurationTools import ConfigurationTools
from ...models import ProductScraped
from location.models import Country
from products.models import Supermarket, Category
from tqdm import tqdm
from whoosh import index
from whoosh.qparser import QueryParser
from scripts.bazar_api_index import PRODUCT_SCHEMA

supermarket = Supermarket(name="Hipercor", zipcode="41009", main_url="https://www.hipercor.es/supermercado/", country=Country.objects.get(code='ESP'))

def supermarket_in_db(supermarket, sqlite_api):
		supermarkets = sqlite_api.get_supermarkets()
		for supermarket_db in supermarkets:
			if supermarket_db[1] == supermarket.name and supermarket_db[2] == supermarket.zipcode and supermarket_db[3] == supermarket.main_url:
				return True
		return False

def get_ean_and_image(product_id):
	
	ix = index.open_dir("data/index", schema=PRODUCT_SCHEMA)

	with ix.searcher() as searcher:
		result = searcher.search(QueryParser("id", schema=PRODUCT_SCHEMA).parse(product_id), limit=1)
		try:
			return (result[0]['ean'], result[0]['image'])
		except:
			try:
				return (result[0]['ean'], "products/images/default.png")
			except:
				return (None, "products/images/default.png")

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)

	category_selector = "body > div.top_menu-container._supermarket > div > nav > p > span"
	category = selenium_utils.get_element_by_css_selector(category_selector).text.strip()

	products = []
	i = 1

	while True:
		print(f"Página 1: {i}")
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')
		common_parent = soup.select('.product_tile.dataholder')

		for item in common_parent:
			id = item.get('data-product-id').strip()
			name = item.select('div.product_tile-right_container > div.product_tile-description_holder > h3 > a')[0].get_text().strip()
			print(name)
			ean, image = get_ean_and_image(id)
			name_link = "https://www.hipercor.es" + item.select('div.product_tile-right_container > div.product_tile-description_holder > h3 > a')[0].get('href').strip()
			try:
				price = item.select('div.product_tile-right_container > div.product_tile-price_holder > div > div > div.prices-price._current')[0].get_text().strip()
				offer_price = None
			except:
				price = item.select('div.product_tile-right_container > div.product_tile-price_holder > div > div > div.prices-price._before')[0].get_text().strip()
				offer_price = item.select('div.product_tile-right_container > div.product_tile-price_holder > div > div > div.prices-price._offer')[0].get_text().strip()
				offer_price = offer_price.replace("€", "").replace(",", ".").strip()
				try:
					offer_price = float(offer_price.split(".")[0] + "." + offer_price.split(".")[1][:2])
				except:
					offer_price = float(offer_price)

			price = price.replace("€", "").replace(",", ".").strip()
			try:
				price = float(price.split(".")[0] + "." + price.split(".")[1][:2])
			except:
				price = float(price)

			try:
				unit_price = item.select('div.product_tile-right_container > div.product_tile-price_holder > div > div > div.prices-price._pum')[0].get_text().strip()
			except:
				unit_price = None

			products.append(ProductScraped(name=name, ean=ean, price=price, offer_price=offer_price , unit_price=unit_price, image=image, is_pack=("pack" in name.lower()), url=name_link, supermarket=supermarket, category=category))

		# Finish pagination configuration in this section

		try:
			i += 1
			print(f"Scraped products: {len(products)}")
			ConfigurationTools.run_pagination_hipercor(selenium_utils)
		except Exception:
			print(f"Scraped products: {len(products)}")
			break
		# -----------------------------------------------

	return products

def scraper(sqlite_api):
	driver_options = webdriver.ChromeOptions()
	driver_options.headless = True
	driver_options.add_argument("start-maximized")
	driver = uc.Chrome(options=driver_options)
	selenium_utils = SeleniumUtils(timeout=10, driver=driver)

	if not supermarket_in_db(supermarket, sqlite_api):
		sql_supermarket = {"name": supermarket.name, "zipcode": supermarket.zipcode, "main_url": supermarket.main_url, "country": supermarket.country.code}
		sqlite_api._add_supermarket(sql_supermarket)
	
	driver.get('https://www.hipercor.es/supermercado/')
	
	#Include the zipcode configuration in this section

	ConfigurationTools.accept_cookies_hipercor(selenium_utils)
	
	#-------------------------------------------------

	tree_paths = ['None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(2)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(3)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(4)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(5)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(6)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(7)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(8)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(9)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(10)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(11)', 'None; body > div.top_menu-container._supermarket > div > nav > a:nth-child(12)'] 

	current_extraction = 1

	for path in tqdm(tree_paths[current_extraction-1:]): 
		
		print(current_extraction)
		products_to_add = extract_data('https://www.hipercor.es/supermercado/', path, driver, selenium_utils)

		sqlite_api.add_products_scraped(products_to_add)

	driver.quit()