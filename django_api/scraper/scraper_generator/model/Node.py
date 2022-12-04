class Node(object):
    
    def __init__(self, selector, parent=None, children=None):
        
        self.set_selector(selector)
        self.set_parent(parent)
        self.set_children(children)
        
        level = 0
        
        if self.get_parent():
            level = self.get_parent().get_level() + 1
        
        self.level = level
        
    def get_child(self, child):
        
        if not isinstance(child, int):
            raise TypeError("Child must be a number")

        if child not in range(len(self.get_children())):
            raise IndexError("Child not found")
        
        return self.get_children()[child]
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, parent):
        
        if parent!=None and not isinstance(parent, Node):
            raise TypeError("Parent must be a Node")
        
        self.parent = parent
    
    def get_selector(self):
        return self.selector
    
    def set_selector(self, selector):
        
        if not isinstance(selector, str):
            raise TypeError("Selector must be a string")
        
        self.selector = selector
    
    def get_children(self):
        return self.children
    
    def set_children(self, children):
        
        if children == None:
            children = []
        
        if not isinstance(children, list):
            raise TypeError("Children must be a list")
        
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
    
    def add(self, name):
        
        if name in self.get_children():
            raise ValueError("Child already exists")
        
        new_node = Node(selector=name, parent=self)
        self.get_children().append(new_node)
        
        return new_node
    
    def calculate_tree_paths(self):
        
        if self.is_leaf():
            return [self.get_selector()]
        else:
            paths = []
            for child in self.get_children():
                paths += [self.get_selector() + "; " + path for path in child.calculate_tree_paths()]
            return paths
    
    def __str__(self):
        
        result = ("\t"*self.get_level()) + str(self.get_selector()) + "\n"
        
        for child in self.get_children():
            result += child.__str__()
        
        return result

    
if __name__ == '__main__':
    
    tree=Node("root")
    print("NEW ROOT (LEVEL=" +  str(tree.get_level()) + "):")
    print(tree)
    print("\n")
    
    tree=tree.add("child1")
    print("NEW CHILD (LEVEL=" +  str(tree.get_level()) + "):")
    print(tree)
    print("\n")
    
    tree=tree.add("grandchild1")
    print("NEW GRANDCHILD (LEVEL=" +  str(tree.get_level()) + "):")
    print(tree)
    print("\n")
    
    tree=tree.get_parent()
    print("CHILD 0 (LEVEL=" +  str(tree.get_level()) + "):")
    print(tree)
    print("\n")
    tree=tree.add("grandchild2")
    print("NEW GRANDCHILD (LEVEL=" +  str(tree.get_level()) + "):")
    print(tree)
    print("\n")
    
    tree=tree.get_parent()
    tree=tree.get_parent()
    print("ROOT (LEVEL=" +  str(tree.get_level()) + ") :")
    print("\n")
    tree=tree.add("child2")
    print("NEW CHILD (LEVEL=" +  str(tree.get_level()) + ") :")
    print(tree)
    print("\n")
    
    tree=tree.get_parent()
    print("ROOT (LEVEL=" +  str(tree.get_level()) + ") :")
    print(tree)
    print("\n")
    
    print("CHILD 0 (LEVEL=" +  str(tree.get_level()) + ") :")
    print(tree.get_child(0))
    print("\n")
    print("CHILD 1 (LEVEL=" +  str(tree.get_level()) + ") :")
    print(tree.get_child(1))
    print("\n")
    
    print("FINAL RESULT:")
    print(tree)
    print("\n")
    paths = tree.calculate_tree_paths()
    print(paths)