class Field(object):
    
    def __init__(self, name=None, selector=None, values=None):
        
        self.set_name(name)
        self.set_selector(selector)
        self.set_values(values)
        
    def __str__(self):
        return "Field[name: %s, selector: %s, values: %s]" % (self.get_name(), self.get_selector(), self.get_values())
    
    # ------------------ GETTERS & SETTERS ------------------ #
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        
        if not isinstance(name, str) and name is not None:
            raise TypeError("name must be a string or None")
        
        self.name = name
        
    def get_selector(self):
        return self.selector
    
    def set_selector(self, selector):
        
        if not isinstance(selector, str):
            raise TypeError("selector must be a string")
        if selector is None:
            raise ValueError("selector cannot be None")
        
        self.selector = selector
        
    def get_values(self):
        return self.values
    
    def set_values(self, values):
        
        if not isinstance(values, list):
            raise TypeError("values must be a list")
        if values is None:
            raise ValueError("values cannot be None")
        
        self.values = values