from bs4 import BeautifulSoup
from ...python_utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
import time

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)

	products_scraped = 0
	while True:
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')
		prices_elements = soup.select('.precio > span')
		prices = [elem.get_text().strip() for elem in prices_elements]
		price_per_kilos_elements = soup.select('.texto-porKilo')
		price_per_kilos = [elem.get_text().strip() for elem in price_per_kilos_elements]
		names_elements = soup.select('.nombre > a')
		names = [elem.get_text().strip() for elem in names_elements]

		data_extracted = zip(prices, price_per_kilos, names)

		for item in data_extracted:

			print("Item[name: %s, price: %s, price_per_kilo: %s]" % (item[2], item[0], item[1]))

			products_scraped += 1

		# Finish pagination configuration in this section
		try:
			next_page_button = [elem for elem in selenium_utils.get_elements_by_css_selector(".activo") if elem.get_attribute("title") == "Siguiente"][0]
			next_page_button.click()
		except:
			print("Se han scrapeado: " + str(products_scraped) + " productos.")
			break
		# -----------------------------------------------
  
def scraper():
	driver_options = webdriver.ChromeOptions()
	driver_options.headless = False
	driver = webdriver.Chrome(options=driver_options)
	selenium_utils = SeleniumUtils(timeout=10, driver=driver)
	
	driver.get('https://www.supermercadoseljamon.com/inicio')
	
	#Include the zipcode configuration in this section
	
	selenium_utils.get_element_by_css_selector("#change-cp").click()
	selenium_utils.get_element_by_css_selector("#seleccionarCp").send_keys("41009")
	selenium_utils.get_element_by_css_selector("#aceptarPorCp").click()
	time.sleep(10)
 
	#-------------------------------------------------

	tree_paths = ['None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(1) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(2) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(3) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(4) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(5) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(6) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(7) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(8) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(9) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(10) > a.link-botcategoria > span', 'None; #banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(11) > a.link-botcategoria > span'] 

	for path in tree_paths: 
		extract_data('https://www.supermercadoseljamon.com/inicio', path, driver, selenium_utils) 
