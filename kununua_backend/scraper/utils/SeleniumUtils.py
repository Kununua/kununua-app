from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class SeleniumUtils(object):
    
    def __init__(self, timeout=10, driver=None):
        
        self.set_timeout(timeout)
        self.set_driver(driver)
        
    def get_element_by_id(self, id):
        
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        
        return WebDriverWait(self.driver, timeout=self.timeout).until(lambda d: d.find_element(by=By.ID, value=id))
    
    def get_element_by_css_selector(self, css_selector, timeout=None):
        
        if not isinstance(css_selector, str):
            raise TypeError("css_selector must be a string")
        
        if timeout:
            return WebDriverWait(self.driver, timeout=timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=css_selector))
        else:
            return WebDriverWait(self.driver, timeout=self.timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value=css_selector))
    
    def get_elements_by_css_selector(self, css_selector, timeout=None):
        
        if not isinstance(css_selector, str):
            raise TypeError("css_selector must be a string")
        
        if timeout:
            return WebDriverWait(self.driver, timeout=timeout).until(lambda d: d.find_elements(by=By.CSS_SELECTOR, value=css_selector))
        else:
            return WebDriverWait(self.driver, timeout=self.timeout).until(lambda d: d.find_elements(by=By.CSS_SELECTOR, value=css_selector))
    
    def get_element_by_text(self, text):
        
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        
        return WebDriverWait(self.driver, timeout=self.timeout).until(lambda d: d.find_element(By.xpath("//*[text()='%s']" % text)))
    
    def navigate_to(self, path):
        
        """
        This method receives a string that containes the elements that must be clicked to navigate to a determined location of the website.
        The string must be in the following format: "object1;object2;object3;...;objectN"
        Each object of the string must be a css_selector of an element that can be clicked.
        """
        
        steps_to_take = path.split(";")
        for step in steps_to_take:
            if step != 'None':  
                element = self.get_element_by_css_selector(step.strip())
                element.click()
        
    def __str__(self):
        return "SeleniumUtils[timeout: %s, driver: %s]" % (self.get_timeout(), self.get_driver())
        
    # ------------------ GETTERS & SETTERS ------------------ #
        
    def get_timeout(self):
        return self.timeout
        
    def set_timeout(self, timeout):
        if not isinstance(timeout, int):
            raise TypeError("timeout must be an integer (the searching timeout in seconds)")
        
        self.timeout = timeout
    
    def get_driver(self):
        return self.driver
    
    def set_driver(self, driver):
         
        if not isinstance(driver, webdriver.Chrome):
            raise TypeError("driver must be a Chrome selenium object")
        
        self.driver = driver