class Node(object):
    
    def __init__(self, selector, parent=None, children=None):
        
        self.set_parent(parent)
        self.set_selector(selector)
        self.set_children(children)
        
        level = 0
        
        if self.get_parent():
            level = self.get_parent().get_level() + 1
        
        self.level = level
        
    def get_child(self, child_index):
        
        if not isinstance(child_index, int):
            raise TypeError("child_index must be a number")

        if child_index not in range(len(self.get_children())):
            raise IndexError("Child not found")
        
        return self.get_children()[child_index]
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, parent):
        
        if parent!=None and not isinstance(parent, Node):
            raise TypeError("Parent must be a Node")
        if parent!=None:
            parent.add_child(self)
        
        self.parent = parent
    
    def get_selector(self):
        return self.selector
    
    def set_selector(self, selector):
        
        if not isinstance(selector, str) and selector is not None:
            raise TypeError("Selector must be a string or None")
        
        if selector is None:
            selector = selector
        else:
            selector = selector.strip()
        parent = self.get_parent()

        if parent is not None and selector in [node.get_selector() for node in parent.get_children() if node is not self]:
            raise ValueError("Selector must be unique")
        
        self.selector = selector
    
    def get_children(self):
        return self.children
    
    def set_children(self, children):
        
        if children == None:
            children = []
        
        if not isinstance(children, list):
            raise TypeError("Children must be a list")
        
        children_set = set(children)
        
        if len(children_set) != len(children):
            children = list(children_set)
        
        self.children = children
    
    def get_level(self):
        return self.level
      
    def is_leaf(self):
        
        if self.get_children():
            return False
        
        return True
    
    def is_root(self):
        
        if self.get_parent():
            return False
        
        return True
    
    def add_child(self, new_node):
        
        if new_node in self.get_children():
            raise ValueError("Child already exists")
        
        self.get_children().append(new_node)
        
        return new_node
    
    def __str__(self):
        
        result = ("\t"*self.get_level()) + str(self.get_selector()) + "\n"
        
        for child in self.get_children():
            result += child.__str__()
        
        return result