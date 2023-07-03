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
        
    # -------------------------------- MERCADONA -------------------------------- #
    
    @staticmethod
    def zipcode_mercadona(selenium_utils):
        selenium_utils.get_element_by_css_selector("#root > header > div > div > form > div > input[type='text']").send_keys("41009")
        selenium_utils.get_element_by_css_selector("#root > header > div > div > form > input").click()
        selenium_utils.get_element_by_css_selector("#root > header > div.header__left > nav > a:nth-child(1)").click()
        
    @staticmethod
    def run_pagination_mercadona(selenium_utils):
        selenium_utils.get_element_by_css_selector("#root > div.grid-layout > div.grid-layout__main-container > div.grid-layout__content > div > div > button", timeout=2).click()
        
    # -------------------------------- CARREFOUR -------------------------------- #
    
    @staticmethod
    def zipcode_carrefour(selenium_utils, driver):
        selenium_utils.get_element_by_id('onetrust-accept-btn-handler').click()
        selenium_utils.get_element_by_css_selector("#app > div > main > div.home-view__main > div.page > div > div > div > div.hst-container-item.cms-distributor-cat > div > div > div > ul > li:nth-child(3) > div > div > a > div:nth-child(2) > h2").click()
        selenium_utils.get_element_by_css_selector("#app > div > nav > div:nth-child(2) > div.wizard.modal-active > div > div > span").click()
        driver.get('https://www.carrefour.es/')
        
    @staticmethod
    def run_pagination_carrefour(selenium_utils, current_page):
        
        selenium_utils.get_element_by_css_selector(".pagination__main").click()
        selenium_utils.get_element_by_css_selector("#app > div > main > div.plp-food-view__main > div.plp-food-view__container > div.plp-food-view__list > div.plp-food-view__results-list-container > div.plp-food-view__pagination > div > div.pagination__container > div.pagination__expandable-content > ul > li:nth-child(%d) > a" % (current_page + 1)).click()
        print("Page passed")
    
    # -------------------------------- DIA -------------------------------- #

    @staticmethod
    def accept_cookies_hipercor(selenium_utils):
        selenium_utils.get_element_by_css_selector("#cookies-agree-all").click()

    @staticmethod
    def run_pagination_hipercor(selenium_utils):
        next_page_button = selenium_utils.get_element_by_css_selector("#pagination-next > a")
        next_page_button.click()