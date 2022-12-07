from .model.Tree import Tree
from .model.Extractors import Extractors
from ..python_utils.SeleniumUtils import SeleniumUtils
from selenium import webdriver
import time
from pathlib import Path

from django.conf import settings


class ScraperGenerator(object):
    
    # TODO se ha añadido el pais como parametro para poder hacer el scraping de cualquier pais
    def __init__(self, url, country, tree, C, driver, elem_details=None, num_pag=None):
        
        self.set_url(url)
        self.set_country(country)
        self.set_tree(tree)
        self.set_C(C)
        self.set_elem_details(elem_details)
        self.set_num_pag(num_pag)
        self.set_driver(driver)
        
    def generate(self):
        
        main_scraper = "def scraper():\n"
        extract_data = "def extract_data(url, path, driver, selenium_utils):\n"
        selenium_utils = SeleniumUtils(timeout=10, driver=self.driver)
        
        main_scraper += self._set_driver_to_scraper(self.get_url())
        self.get_driver().get(self.get_url())
        
        # zipcode configuration section
        
        selenium_utils.get_element_by_css_selector("#change-cp").click()
        selenium_utils.get_element_by_css_selector("#seleccionarCp").send_keys("41009")
        selenium_utils.get_element_by_css_selector("#aceptarPorCp").click()
        time.sleep(10)
        
        # -----------------------------
        
        tree_paths = self.get_tree().calculate_tree_paths()
        main_scraper += "\ttree_paths = %s \n" % (tree_paths)
        main_scraper += "\n"
        main_scraper += "\tfor path in tree_paths: \n"
        main_scraper += "\t\textract_data('%s', path, driver, selenium_utils) \n" % (self.get_url())
        
        extract_data += "\tdriver.get(url)\n"
        extract_data += "\tselenium_utils.navigate_to(path)\n"
        extract_data += "\n"
        
        selenium_utils.navigate_to(tree_paths[0])
        
        extractor = Extractors(C=self.C, extract_data=extract_data, driver=self.driver, driver_utils=selenium_utils)
        get_urls_to_extract = None
        if self.elem_details is None:
            fields_to_be_extracted = extractor.standard_extraction()
        else:
            fields_to_be_extracted = extractor.recursive_extraction(self.elem_details, self.num_pag)
            get_urls_to_extract = self._create_get_urls_to_extract_method()
            
        fields_to_be_extracted = self.perform_matching(fields_to_be_extracted)
        
        extract_data = extractor.update_extraction_function(extract_data, fields_to_be_extracted)
        self.create_scraper_file(main_scraper, extract_data, get_urls_to_extract)
        
        
    def perform_matching(self, fields_to_be_extracted):
        
        field_counter = 1
        result = []
        
        for field in fields_to_be_extracted:
            
            field_name = input("The field %i has the following values: %s\nPlease, enter the name of the field (or write x to discard): " % (field_counter, field.get_values()))

            if field_name != 'x':
                field.set_name(field_name)
                result.append(field)
                print("The name of the field has been set to: %s \n" % (field_name))
        
        return result
    
    def create_scraper_file(self, main_scraper, extract_data, get_urls_to_extract=None):
        
        path = Path(str(settings.BASE_DIR) + "/scraper/scrapers/%s" % (self.get_country().lower()))
        
        path.mkdir(parents=True, exist_ok=True)
        
        with open (str(path) + "/generated_scraper_%s.py" % str(time.time()).split(".")[0], "w") as f:
            
            f.write(self._initial_configuration())
            if get_urls_to_extract is not None:
                f.write(get_urls_to_extract)
            f.write(extract_data)
            f.write(main_scraper)
            f.close()
        
    def __str__(self):
        return "ScraperGenerator[url: %s]" % (self.get_url())
    
    # ------------------ PRIVATE FUNCTIONS ------------------ #
    
    def _initial_configuration(self):
        
        result = "from bs4 import BeautifulSoup\n"
        result += "from ...python_utils.SeleniumUtils import SeleniumUtils\n"
        result += "from selenium import webdriver\n"
        result += "import time\n"
        result += "\n"
        
        return result
    
    def _create_get_urls_to_extract_method(self):
        get_urls_to_extract = "def get_urls_to_extract(selenium_utils):\n"
        get_urls_to_extract += "\n"
        get_urls_to_extract += "\tlocated_elements = selenium_utils.get_elements_by_css_selector('%s')\n" % self.elem_details
        get_urls_to_extract += "\n"
        get_urls_to_extract += "\treturn [elem.get_attribute('href') for elem in located_elements]\n"
        get_urls_to_extract += "\n"
        
        return get_urls_to_extract
    
    # ------------------ GETTERS & SETTERS ------------------ #
    
    def get_url(self):
        return self.url
    
    def set_url(self, url):
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        self.url = url
        
    def get_country(self):
        return self.country
        
    def set_country(self, country):
        
        if not isinstance(country, str):
            raise TypeError("country must be a string")
        
        self.country = country
    
    def get_tree(self):
        return self.tree
    
    def set_tree(self, tree):
        
        if not isinstance(tree, Tree):
            raise TypeError("tree must be a Tree object")
        
        self.tree = tree
        
    def get_C(self):
        return self.C
    
    def set_C(self, C):
        if not isinstance(C, list):
            raise TypeError("C must be a list")
        self.C = C
        
    def get_elem_details(self):
        return self.elem_details
    
    def set_elem_details(self, elem_details):
        if not isinstance(elem_details, str) and elem_details is not None:
            raise TypeError("elem_details must be a string or None")
        self.elem_details = elem_details
        
    def get_num_pag(self):
        return self.num_pag
    
    def set_num_pag(self, num_pag):
        
        if self.elem_details is not None and num_pag is None:
            raise ValueError("num_pag must be specified if elem_details is specified")
        elif self.elem_details is None and num_pag is not None:
            raise ValueError("if elem_details is not specified, num_pag must be None")
        elif not isinstance(num_pag, int) and num_pag is not None:
            raise TypeError("num_pag must be an integer or None")
        elif num_pag < 0 and num_pag is not None:
            raise ValueError("num_pag must be a positive integer or None")
        
        self.num_pag = num_pag
        
    def get_driver(self):
        return self.driver
    
    def set_driver(self, driver):
        
        if not isinstance(driver, webdriver.Chrome):
            raise TypeError("driver must be a chrome selenium driver")
        
        self.driver = driver
        
    # ------------------ PRIVATE METHODS ------------------ #
    
    def _set_driver_to_scraper(self, url):
        
        text_to_add = "\tdriver_options = webdriver.ChromeOptions()\n"
        text_to_add += "\tdriver_options.headless = False\n"
        text_to_add += "\tdriver = webdriver.Chrome(options=driver_options)\n"
        text_to_add += "\tselenium_utils = SeleniumUtils(timeout=10, driver=driver)\n"
        text_to_add += "\t\n"
        text_to_add += "\tdriver.get('%s')\n" % (url)
        text_to_add += "\t\n"
        text_to_add += "\t#Include the zipcode configuration in this section\n"
        text_to_add += "\t\n"
        text_to_add += "\t#-------------------------------------------------\n"
        text_to_add += "\n"
        
        return text_to_add