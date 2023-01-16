from bs4 import BeautifulSoup
from ...python_utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
import time

def get_urls_to_extract(selenium_utils):

	located_elements = selenium_utils.get_elements_by_css_selector('p.nombre > a')

	return [elem.get_attribute('href') for elem in located_elements]

def extract_data(url, path, driver, selenium_utils):
	driver.get(url)
	selenium_utils.navigate_to(path)

	url_cache = driver.current_url
	products_scraped = 0
	while True:
		urls_to_extract = get_urls_to_extract(selenium_utils)
		for url_to_extract in urls_to_extract:
			driver.get(url_to_extract)
			page_source = driver.page_source
			soup = BeautifulSoup(page_source, 'lxml')
			nombre = soup.select_one('#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > h1').get_text().strip()
			marca = soup.select_one('#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > span').get_text().strip()
			try:
				denominacion = soup.select_one('#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div > ul > li > img').get('src').strip()
			except:
				denominacion = None
    
			precio = soup.select_one('#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div > div > span').get_text().strip()

			print("[name:%s, brand:%s, price:%s, denominacion: %s]" % (nombre, marca, precio, denominacion))

			products_scraped += 1

		driver.get(url_cache)
		selenium_utils.navigate_to(path)

		# Finish pagination configuration in this section
		try:
			next_page_button = [elem for elem in selenium_utils.get_elements_by_css_selector(".activo") if elem.get_attribute("title") == "Siguiente"][0]
			next_page_button.click()
			url_cache = driver.current_url
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
