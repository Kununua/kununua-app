from .Field import Field

from selenium import webdriver
from selenium.webdriver.common.by import By
from ...utils.SeleniumUtils import SeleniumUtils

class Extractors(object):
    
    def __init__(self, C=None, extract_data=None, driver=None, driver_utils=None, common_parent_selector=None):
        
        self.set_C(C)
        self.set_extract_data(extract_data)
        self.set_driver(driver)
        self.set_driver_utils(driver_utils)
        self.set_common_parent_selector(common_parent_selector)
        self.data_lists_to_zip = ""
        self.multifield_counter = 1
        
    def standard_extraction(self):
        
        leaves_selectors = self._get_dom_leaves_selectors(self.get_C())
        data_dict = {}
        
        for leaf in leaves_selectors:
            
            matched_leaves = self.get_driver_utils().get_elements_by_css_selector(leaf)
            
            for matched_leaf in matched_leaves:
                if leaf not in data_dict.keys():
                    data_dict[leaf] = []
                
                relative_leaf_values = data_dict[leaf]
                if matched_leaf.tag_name == "img":
                    relative_leaf_values.append(matched_leaf.get_attribute("src"))
                else:
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
                leaf_value = None
                try:
                    if leaf_selector.endswith("img"):
                        try:
                            leaf = self.get_driver_utils().get_element_by_css_selector(leaf_selector)
                            leaf_value = leaf.get_attribute("src")
                        except Exception:
                            leaf_value = None
                    else:
                        leaf = self.get_driver_utils().get_element_by_css_selector(leaf_selector)
                        leaf_value = leaf.text
                        
                    leaf_values.append(leaf_value)
                except Exception:
                    continue
        
        self._prepare_function_to_recursive_extraction()
        
        fields_to_be_extracted = self._get_fields_to_be_extracted(data_dict)
        
        return fields_to_be_extracted
    
    def update_standard_extraction_function(self, fields_to_be_extracted):
        
        extract_data_function = self.get_extract_data()
        
        for field in fields_to_be_extracted:
            
            if not self.common_parent_selector:
                field_extraction = self.standard_field_extraction_with_no_common_parent(field)
                extract_data_function += field_extraction
                
            else:
                
                field_extraction = self.standard_field_extraction_with_common_parent(field)
                extract_data_function += field_extraction
                
        if not self.common_parent_selector:
            extract_data_function += "\n"
            extract_data_function += "\t\tdata_extracted = itertools.zip_longest(%s)\n" % self.data_lists_to_zip[:-2]
            extract_data_function += "\n"
            extract_data_function += "\t\tfor item in data_extracted:\n"
            extract_data_function += "\n"
            extract_data_function += "\t\t\t# Write print or save data function on this line \n"
            extract_data_function += "\n"
            extract_data_function += "\t\t\tproducts_scraped += 1\n"
            extract_data_function += "\n"
        else:
            extract_data_function += "\n"
            extract_data_function += "\t\t\tproducts_scraped += 1"
            extract_data_function += "\n"
            extract_data_function += "\t\t\t# Write print or save data function on this line\n"
            extract_data_function += "\n"
            
        extract_data_function += "\t\t# Finish pagination configuration in this section\n"
        extract_data_function += "\n"
        extract_data_function += "\t\t# -----------------------------------------------\n"
        extract_data_function += "\n"
        
        return extract_data_function
    
    def update_recursive_extraction_function(self, fields_to_be_extracted):
        
        extract_data_function = self.get_extract_data()
        multifield_counter = 1
        
        for field in fields_to_be_extracted:
            
            if "," in field.get_name():
                value_separator = field.get_name().split("(")[1].split(")")[0]
                field_names = [name.strip() for name in field.get_name().split("(")[0].split(",")]
                main_value = field.get_name().split("[")[1].split("]")[0]
                
                extract_data_function += "\t\t\tmultifield_%s_data = tuple(soup.select_one('%s').get_text().strip().split('%s'))\n" % (str(multifield_counter), field.get_selector(), value_separator)
                extract_data_function += "\t\t\t"
                default_tuple = "("
                
                for name in field_names:
                    extract_data_function += "%s, " % name
                    if name == main_value:
                        default_tuple += "soup.select_one('%s').get_text().strip(), " % field.get_selector()
                    else:
                        default_tuple += "None, "
                        
                default_tuple = default_tuple[:-2]
                default_tuple += ")"
                extract_data_function = extract_data_function[:-2]
                extract_data_function += " = multifield_%s_data if len(multifield_%s_data) == %s else %s\n" % (str(multifield_counter), str(multifield_counter), str(len(field_names)), default_tuple)
                
                multifield_counter += 1
                
            else:
                if field.get_selector().endswith("img"):
                    extract_data_function += "\t\t\ttry:\n"
                    extract_data_function += "\t\t\t\t%s = soup.select_one('%s').get('src').strip()\n" % (field.get_name(), field.get_selector())
                    extract_data_function += "\t\t\texcept Exception:\n"
                    extract_data_function += "\t\t\t\t%s = None\n" % (field.get_name())
                else:
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
        if self.common_parent_selector is not None:
            self.extract_data += "\t\tcommon_parent = soup.select('%s')\n" % self.common_parent_selector
            self.extract_data += "\t\tfor item in common_parent:\n"
    
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
        leaves += [img for img in container.find_elements(by = By.TAG_NAME, value = "img") if img.get_attribute("src") != ""]
        
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
    
    def standard_field_extraction_with_no_common_parent(self, field):
        
        result = ""
        
        if "," in field.get_name():
            result += "\t\tmultifield_%s_elements = soup.select('%s')\n" % (str(self.multifield_counter), field.get_selector())
            value_separator = field.get_name().split("(")[1].split(")")[0]
            field_names = [name.strip() for name in field.get_name().split("(")[0].split(",")]
            main_value = field.get_name().split("[")[1].split("]")[0]
            default_tuple = "("
            parsing_row = "\t\t"
            
            for name in field_names:
                parsing_row += "%ss, " % name
                self.set_data_lists_to_zip(self.data_lists_to_zip + "%ss, " % name)
                if name == main_value:
                    default_tuple += "elem.get_text().strip(), "
                else:
                    default_tuple += "None, "
            
            default_tuple = default_tuple[:-2]
            default_tuple += ")"
                    
            parsing_row = parsing_row[:-2]
            result +=  "\t\tmultifield_%s_values = [tuple(elem.get_text().strip().split('%s')) if len(elem.get_text().strip().split('%s')) == %s else %s for elem in multifield_%s_elements]\n" % (str(self.multifield_counter), value_separator, value_separator, str(len(field_names)), default_tuple, str(self.multifield_counter))
            result += parsing_row
            result += " = tuple([list(t) for t in zip(*multifield_%s_values)])\n" % str(self.multifield_counter)
            
            if field.get_selector().endswith("> a"):
                result +=  "\t\t%ss_links = [elem.get('href').strip() for elem in multifield_%s_elements]\n" % (main_value, str(self.multifield_counter))
            
            self.set_multifield_counter(self.multifield_counter+1)
                
        else:
            result +=  "\t\t%ss_elements = soup.select('%s')\n" % (field.get_name(), field.get_selector())
            if field.get_selector().endswith("img"):
                result +=  "\t\t%ss = [elem.get('src').strip() for elem in %ss_elements]\n" % (field.get_name(), field.get_name())
            elif field.get_selector().endswith("> a"):
                result +=  "\t\t%ss_links = [elem.get('href').strip() for elem in %ss_elements]\n" % (field.get_name(), field.get_name())
            else:
                result +=  "\t\t%ss = [elem.get_text().strip() for elem in %ss_elements]\n" % (field.get_name(), field.get_name())
            self.set_data_lists_to_zip(self.data_lists_to_zip + "%ss, " % field.get_name())
        
        return result
    
    def standard_field_extraction_with_common_parent(self, field):
        
        result = ""
        
        if "," in field.get_name():
            result += "\t\t\tmultifield_%s = item.select('%s')[0]\n" % (str(self.multifield_counter), field.get_selector())
            value_separator = field.get_name().split("(")[1].split(")")[0]
            field_names = [name.strip() for name in field.get_name().split("(")[0].split(",")]
            main_value = field.get_name().split("[")[1].split("]")[0]
            default_tuple = "("
            parsing_row = "\t\t\t"
            
            for name in field_names:
                parsing_row += "%s, " % name
                if name == main_value:
                    default_tuple += "multifield_%s.get_text().strip(), " % str(self.multifield_counter)
                else:
                    default_tuple += "None, "
            
            default_tuple = default_tuple[:-2]
            default_tuple += ")"
                    
            parsing_row = parsing_row[:-2]
            result += parsing_row
            result +=  " = tuple(multifield_%s.get_text().strip().split('%s') if len(multifield_%s.get_text().strip().split('%s')) == %s else %s)\n" % (str(self.multifield_counter), value_separator, str(self.multifield_counter), value_separator, str(len(field_names)), default_tuple)
            
            if field.get_selector().endswith("> a"):
                result +=  "\t\t\t%s_link = multifield_%s.get('href').strip()\n" % (main_value, str(self.multifield_counter))
            
            self.set_multifield_counter(self.multifield_counter+1)
                
        else:
            if field.get_selector().endswith("img"):
                result +=  "\t\t\t%s = item.select('%s')[0].get('src').strip()\n" % (field.get_name(), field.get_selector())
            elif field.get_selector().endswith("> a"):
                result +=  "\t\t\t%s_link = item.select('%s')[0].get('href').strip()\n" % (field.get_name(), field.get_selector())
            else:
                result +=  "\t\t\t%s = item.select('%s')[0].get_text().strip()\n" % (field.get_name(), field.get_selector())
                
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
        
    def get_common_parent_selector(self):
        return self.common_parent_selector
    
    def set_common_parent_selector(self, common_parent_selector):
        
        if not isinstance(common_parent_selector, str):
            raise TypeError("common_parent_selector must be a string")
        
        self.common_parent_selector = common_parent_selector
        
    def get_multifield_counter(self):
        return self.multifield_counter
    
    def set_multifield_counter(self, multifield_counter):
        
        if not isinstance(multifield_counter, int):
            raise TypeError("multifield_counter must be an integer")
        
        self.multifield_counter = multifield_counter
        
    def get_data_lists_to_zip(self):
        return self.data_lists_to_zip
        
    def set_data_lists_to_zip(self, data_lists_to_zip):
        
        if not isinstance(data_lists_to_zip, str):
            raise TypeError("data_lists_to_zip must be a string")
        
        self.data_lists_to_zip = data_lists_to_zip