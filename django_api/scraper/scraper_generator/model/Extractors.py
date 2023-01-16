from .Field import Field

from selenium import webdriver
from selenium.webdriver.common.by import By
from ...python_utils.SeleniumUtils import SeleniumUtils

class Extractors(object):
    
    def __init__(self, C=None, extract_data=None, driver=None, driver_utils=None):
        
        self.set_C(C)
        self.set_extract_data(extract_data)
        self.set_driver(driver)
        self.set_driver_utils(driver_utils)
        
    def standard_extraction(self):
        
        leaves_selectors = self._get_dom_leaves_selectors(self.get_C())
        data_dict = {}
        
        for leaf in leaves_selectors:
            
            matched_leaves = self.get_driver_utils().get_elements_by_css_selector(leaf)
            
            for matched_leaf in matched_leaves:
                if leaf not in data_dict.keys():
                    data_dict[leaf] = []
                
                relative_leaf_values = data_dict[leaf]
                relative_leaf_values.append(matched_leaf.text)
                
        self._prepare_function_to_standard_extraction()
        
        fields_to_be_extracted = self._get_fields_to_be_extracted(data_dict)
        
        return fields_to_be_extracted
    
    def recursive_extraction(self, elem_details, num_pag):
        
        detail_pages_urls = self._locate_detail_pages(elem_details, num_pag)
        leaves_selectors = []
        data_dict = {}
        first_iteration = True
        
        for detail_page_url in detail_pages_urls:
            self.get_driver().get(detail_page_url)
            
            if first_iteration:
                leaves_selectors = self._get_dom_leaves_selectors(self.get_C())
                first_iteration = False
                
            for leaf_selector in leaves_selectors:
                
                if leaf_selector not in data_dict.keys():
                    data_dict[leaf_selector] = []
                
                leaf_values = data_dict[leaf_selector]
                leaf_values.append(self.get_driver_utils().get_element_by_css_selector(leaf_selector).text)
        
        self._prepare_function_to_recursive_extraction()
        
        fields_to_be_extracted = self._get_fields_to_be_extracted(data_dict)
        
        return fields_to_be_extracted
    
    def update_standard_extraction_function(self, extract_data_function, fields_to_be_extracted):
        
        extract_data_function = self.get_extract_data()
        data_lists_to_zip = ""
        
        for field in fields_to_be_extracted:
            
            extract_data_function += "\t\t%ss_elements = soup.select('%s')\n" % (field.get_name(), field.get_selector())
            extract_data_function += "\t\t%ss = [elem.get_text().strip() for elem in %ss_elements]\n" % (field.get_name(), field.get_name())
            data_lists_to_zip += "%ss, " % field.get_name()
        
        extract_data_function += "\n"
        extract_data_function += "\t\tdata_extracted = zip(%s)\n" % data_lists_to_zip[:-2]
        extract_data_function += "\n"
        extract_data_function += "\t\tfor item in data_extracted:\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t\t # Write print or save data function on this line \n"
        extract_data_function += "\n"
        extract_data_function += "\t\t\tproducts_scraped += 1\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t# Finish pagination configuration in this section\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t# -----------------------------------------------\n"
        extract_data_function += "\n"
        
        return extract_data_function
    
    def update_recursive_extraction_function(self, extract_data_function, fields_to_be_extracted):
        
        extract_data_function = self.get_extract_data()
        
        for field in fields_to_be_extracted:
            
            extract_data_function += "\t\t\t%s = soup.select_one('%s').get_text().strip()\n" % (field.get_name(), field.get_selector())
        
        extract_data_function += "\n"
        extract_data_function += "\t\t\t# Write print or save data function on this line\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t\tproducts_scraped += 1\n"
        extract_data_function += "\n"
        extract_data_function += "\t\tdriver.get(url_cache)\n"
        extract_data_function += "\t\tselenium_utils.navigate_to(path)\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t# Finish pagination configuration in this section\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t# -----------------------------------------------\n"
        extract_data_function += "\n"
        
        return extract_data_function
    
    def __str__(self):
        return "Extractors[C: %s, extract_data: %s, driver: %s]" % (self.get_C(), self.get_extract_data(), self.get_driver())
    
    # ------------------ PRIVATE FUNCTIONS ------------------ #
    
    def _prepare_function_to_standard_extraction(self):

        self.extract_data += "\t\tpage_source = driver.page_source\n"
        self.extract_data += "\t\tsoup = BeautifulSoup(page_source, 'lxml')\n"
    
    def _prepare_function_to_recursive_extraction(self):

        self.extract_data += "\t\turls_to_extract = get_urls_to_extract(selenium_utils)\n"
        self.extract_data += "\t\tfor url_to_extract in urls_to_extract:\n"
        self.extract_data += "\t\t\tdriver.get(url_to_extract)\n"
        self.extract_data += "\t\t\tpage_source = driver.page_source\n"
        self.extract_data += "\t\t\tsoup = BeautifulSoup(page_source, 'lxml')\n"
        
    def _locate_detail_pages(self, elem_details, num_pag):
        
        located_elements = self.get_driver_utils().get_elements_by_css_selector(elem_details)[:num_pag]
        
        # TODO revisar, puede no ser siempre a con href
        
        return [elem.get_attribute("href") for elem in located_elements]
    
    def _get_dom_leaves_selectors(self, C):
        
        result = []
        
        for container_selector in C:
            
            container = self.get_driver_utils().get_element_by_css_selector(container_selector)
            
            result = result + self._get_leaves_from_container(container, container_selector)
        
        return result
    
    def _get_leaves_from_container(self, container, container_selector):
        
        leaves = [leaf for leaf in container.find_elements(by = By.XPATH, value = ".//*[not(*)]") if leaf.text.strip() != ""]  
        
        if len(leaves) == 0:
            leaves = [container]
        
        result = set()
        
        for leaf in leaves:
            
            leaf_selector = self._build_leaf_selector(leaf, container, container_selector)
            
            result.add(leaf_selector.strip())
        
        return list(result)
        
    def _build_leaf_selector(self, leaf, container, container_selector):
        
        if leaf == container:
            return container_selector
        else:
            return self._build_leaf_selector(leaf.find_element(by = By.XPATH, value=".."), container, container_selector) + " > " + leaf.tag_name
        
    def _get_fields_to_be_extracted(self, data_dict):
        
        # TODO revisar con profesor
        
        keys_to_delete = []
        result = []
        
        for key in data_dict.keys():
            if len(set(data_dict[key])) == 1:
                keys_to_delete.append(key)
        
        for key_to_delete in keys_to_delete:
            data_dict.pop(key_to_delete)

        for key in data_dict.keys():
            field = Field(name=None, selector=key, values=data_dict[key])
            result.append(field)
        
        return result
    
    # ------------------ GETTERS & SETTERS ------------------ #
    
    def get_C(self):
        return self.C
    
    def set_C(self, C):
        
        if not isinstance(C, list):
            raise TypeError("C must be a list")
        if C is None:
            raise ValueError("C cannot be None")
        
        self.C = C
        
    def get_extract_data(self):
        return self.extract_data
    
    def set_extract_data(self, extract_data):
        
        if not isinstance(extract_data, str):
            raise TypeError("extract_data must be a string")
        if extract_data is None:
            raise ValueError("extract_data cannot be None")
        
        self.extract_data = extract_data
    
    def get_driver(self):
        return self.driver
    
    def set_driver(self, driver):
        
        if not isinstance(driver, webdriver.Chrome):
            raise TypeError("driver must be a chrome selenium driver")
        if driver is None:
            raise ValueError("driver cannot be None")
        
        self.driver = driver
        
    def get_driver_utils(self):
        return self.driver_utils
    
    def set_driver_utils(self, driver_utils):
        
        if not isinstance(driver_utils, SeleniumUtils):
            raise TypeError("driver_utils must be a SeleniumUtils object")
        
        if driver_utils is None:
            raise ValueError("driver_utils cannot be None")
        
        self.driver_utils = driver_utils