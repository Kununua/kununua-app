from bs4 import BeautifulSoup
from ...utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
from ...configuration_tools import ConfigurationTools
import itertools

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)

	products_scraped = 0
	while True:
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')
		common_parent = soup.select('.articulo')
		for item in common_parent:
			brand = item.select('.marca')[0].get_text().strip()
			multifield_1 = item.select('.nombre > a')[0]
			name, quantity = tuple(multifield_1.get_text().strip().split(',') if len(multifield_1.get_text().strip().split(',')) == 2 else (multifield_1.get_text().strip(), None))
			name_link = multifield_1.get('href').strip()
			price = item.select('.precio > span')[0].get_text().strip()
			unit_price = item.select('.texto-porKilo')[0].get_text().strip()
			product_image = item.select('.imgwrap > img')[0].get('src').strip()

			products_scraped += 1
			print("Brand: %s, Name: %s, Quantity: %s, Name Link: %s, Price: %s, Unit Price: %s, Product Image: %s" % (brand, name, quantity, name_link, price, unit_price, product_image))

		# Finish pagination configuration in this section
		try:
			ConfigurationTools.run_pagination_eljamon(selenium_utils)
		except Exception:
      
			print("Products scraped: %d" % products_scraped)
			break
		# -----------------------------------------------

def scraper():
	driver_options = webdriver.ChromeOptions()
	driver_options.headless = False
	driver = webdriver.Chrome(options=driver_options)
	selenium_utils = SeleniumUtils(timeout=10, driver=driver)
	
	driver.get('https://www.supermercadoseljamon.com/inicio')
	
	#Include the zipcode configuration in this section
	ConfigurationTools.zipcode_eljamon(selenium_utils)
	#-------------------------------------------------

	tree_paths = ['None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(1) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(2) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(3) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(4) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(5) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(6) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(7) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(8) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(9) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(10) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(11) > a.link-botcategoria > span'] 

	for path in tree_paths: 
		extract_data('https://www.supermercadoseljamon.com/inicio', path, driver, selenium_utils) 
