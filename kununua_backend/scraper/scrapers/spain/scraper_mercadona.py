from bs4 import BeautifulSoup
from ...utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
from ...utils.ConfigurationTools import ConfigurationTools
from ...utils.ProductShelf import ProductShelf
from ...models import ProductScraped
from products.models import Supermarket, Category
from location.models import Country
from tqdm import tqdm
import time

supermarket = Supermarket(name="Mercadona", zipcode="41009", main_url="https://www.mercadona.es", country=Country.objects.get(code='ESP'))
# def get_element_url(selenium_utils, driver, element, grid_url):
#     element.click()
#     url = driver.current_url
#     selenium_utils.get_element_by_css_selector('#root > div.ui-focus-trap > div > div:nth-child(2) > div > div.modal-content__header > button').click()
#     selenium_utils.get_element_by_css_selector('.product-cell')
#     return url

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)

	products = []
	category_selector = path.split(';')[-1].strip()

	while True:
		selenium_utils.get_element_by_css_selector('.product-cell')
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')
		common_parent = soup.select('.product-cell')
		# web_elements = selenium_utils.get_elements_by_css_selector('.product-cell')
		# grid_url = driver.current_url
		for i in range(len(common_parent)):
			item = common_parent[i]
			# element = web_elements[i]
			name = item.select('.product-cell__description-name')[0].get_text().strip()
			price = float(item.select('.product-price__unit-price')[0].get_text().split(' ')[0].replace(',','.').strip())
			try:
				weight = item.select('button > div.product-cell__info > div.product-format.product-format__size--cell > span:nth-child(2)')[0].get_text().strip()
			except Exception:
				weight = item.select('.footnote1-r')[0].get_text().strip()
			image = item.select('button > div.product-cell__image-wrapper > img')[0].get('src').strip()
			category = soup.select(category_selector)[0].get_text().strip()
			is_pack = "pack" in item.select(".product-price__extra-price")[0].get_text().lower()
			#url = get_element_url(selenium_utils, driver, element, grid_url)

			product = ProductScraped(name=name, price=price, weight=weight, image=image, is_pack=is_pack, url=None, supermarket=supermarket, category=Category(name=category))
   
			products.append(product)
		# Finish pagination configuration in this section
		try:
			ConfigurationTools.run_pagination_mercadona(selenium_utils)
		except Exception:
			break
		# ----------------------------------------------

	return products

def scraper():
	driver_options = webdriver.ChromeOptions()
	driver_options.headless = False
	driver = webdriver.Chrome(options=driver_options)
	selenium_utils = SeleniumUtils(timeout=10, driver=driver)
	
	driver.get('https://www.mercadona.es')
	
	#Include the zipcode configuration in this section
	
	ConfigurationTools.zipcode_mercadona(selenium_utils)
	selenium_utils.get_element_by_css_selector('.cookie-banner > div > div > button.ui-button.ui-button--small.ui-button--primary.ui-button--positive').click()
	#-------------------------------------------------

	tree_paths = ['.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(1) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(2) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(3) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(4) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(5) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(6) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(7) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(8) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(9) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(10) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(11) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(12) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(13) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(14) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(15) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(16) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(17) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(18) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(19) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(20) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(21) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(22) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(23) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(24) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(25) > div > button > span > label', '.menu-item; #root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(26) > div > button > span > label'] 

	products = []
 
	print("Extracting data...")

	for path in tqdm(tree_paths): 
		products_to_add = extract_data('https://tienda.mercadona.es', path, driver, selenium_utils) 

		products += products_to_add
  
	driver.quit()
 
	shelve_util = ProductShelf('data/shelves/new-products-scraped')
	shelve_util.create_shelf(products)