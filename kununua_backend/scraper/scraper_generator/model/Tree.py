from .Node import Node
import logging

class Tree(object):
        
    def __init__(self, nodes=None):
        
        if not nodes: nodes = []
        
        if not isinstance(nodes, list):
            raise TypeError("Nodes must be a list")
        
        self.nodes = nodes
        
    def get_root(self):
        return self.nodes[0]
    
    def add(self, new_node):
        
        if not isinstance(new_node, Node):
            raise ValueError("new_node must be a Node object")
        
        if new_node.get_parent() != None and not self.nodes:
            raise ValueError("The tree first node of the tree must not have a parent")
        
        if new_node.get_parent() == None and self.nodes:
            raise ValueError("The tree does already have a root node")
        
        self.nodes.append(new_node)
        
        logging.info("Node '%s' added to the tree on level %i" % (new_node.get_selector(), new_node.get_level()))
    
    def calculate_tree_paths(self):
        
        root_node = self.get_root()
        
        return self._calculate_tree_paths_recursive(root_node)
    
    def reset_tree(self):
        self.nodes = []
    
    def _calculate_tree_paths_recursive(self, node):
        
        if node.is_leaf():
            return [node.get_selector()]
        else:
            paths = []
            for child in node.get_children():
                paths += [str(node.get_selector()) + "; " + path for path in self._calculate_tree_paths_recursive(child)]
            return paths
    
    def __str__(self):
        
        if len(self.nodes) == 0:
            return "Tree is empty"
        root_node = self.get_root()
        
        result = ("\t"*root_node.get_level()) + str(root_node.get_selector()) + "\n"
        
        for child in root_node.get_children():
            result += child.__str__()
        
        return result