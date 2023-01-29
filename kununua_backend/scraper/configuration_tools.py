import time

class ConfigurationTools():
    
    # -------------------------------- EL JAMÓN -------------------------------- #
    
    @staticmethod
    def zipcode_eljamon(selenium_utils):
        selenium_utils.get_element_by_css_selector("#change-cp").click()
        selenium_utils.get_element_by_css_selector("#seleccionarCp").send_keys("41009")
        selenium_utils.get_element_by_css_selector("#aceptarPorCp").click()
        time.sleep(5)
        
    @staticmethod
    def run_pagination_eljamon(selenium_utils):
        
        next_page_button = [elem for elem in selenium_utils.get_elements_by_css_selector(".activo") if elem.get_attribute("title") == "Siguiente"][0]
        next_page_button.click()
		