from pathlib import Path
from django.test import TestCase
from .scraper_generator.model.Node import Node
from .scraper_generator.model.Tree import Tree
from .scraper_generator.ScraperGenerator import ScraperGenerator
from .python_utils.Timer import Timer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from django.conf import settings

from .scrapers.spain import generated_scraper_plantilla_recursivo as recursive_scraper
from .scrapers.spain import generated_scraper_plantilla_standard as standard_scraper
class TreeTestCase(TestCase):
    def setUp(self):
        timer = Timer()
        timer.start()
        self.tree = Tree()
    
        root = Node(selector="root")
        child1 = Node(selector="child1", parent=root)
        child2 = Node(selector="child2", parent=root)
        grandchild1 = Node(selector="grandchild1", parent=child1)
        grandchild2 = Node(selector="grandchild2", parent=child1)
        
        self.tree.add(root)
        self.tree.add(child1)
        self.tree.add(child2)
        self.tree.add(grandchild1)
        self.tree.add(grandchild2)
        
        self.timer = timer
        self.root = root
    
    def test_calculate_tree_paths(self):
        print("FINAL RESULT:")
        print(self.tree)
        print("\n")
        paths = self.tree.calculate_tree_paths()
        print(paths)
        self.timer.stop()
        print("El tiempo de ejecución ha sido de %f milisegundos" % (self.timer.get_time()))
        
    def test_calculate_tree_paths_with_null_root_selector(self):
        
        self.root.set_selector(None)
        
        print("FINAL RESULT:")
        print(self.tree)
        print("\n")
        paths = self.tree.calculate_tree_paths()
        print(paths)
        self.timer.stop()
        print("El tiempo de ejecución ha sido de %f milisegundos" % (self.timer.get_time()))
        
class GeneratorElJamonRecursiveCase(TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = False # Change to True if you want to run the scraper in headless mode
        self.driver = webdriver.Chrome(options=options)
        
        tree_el_jamon = self.generate_tree_for_el_jamon()
        
        self.generator = ScraperGenerator(url="https://www.supermercadoseljamon.com/inicio", 
                                          country="Spain",
                                          tree=tree_el_jamon, 
                                          C=["#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos"], 
                                          driver=self.driver, 
                                          elem_details="p.nombre > a", 
                                          num_pag=5)
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
    
    def test_generate_scraper_for_el_jamon(self):
        self.driver.get(self.generator.get_url())
        self.generator.generate()
        
    def generate_tree_for_el_jamon(self):
        
        result_tree = Tree()
        
        root = Node(selector=None, parent=None)
        result_tree.add(root)
        for i in range(11):
            child = Node(selector="#banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(%d) > a.link-botcategoria > span" % (i+1), parent=root)
            result_tree.add(child)

        return result_tree
    
class GeneratorElJamonStandardCase(TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = False # Change to True if you want to run the scraper in headless mode
        self.driver = webdriver.Chrome(options=options)
        
        tree_el_jamon = self.generate_tree_for_el_jamon()
        
        self.generator = ScraperGenerator(url="https://www.supermercadoseljamon.com/inicio", 
                                          country="Spain",
                                          tree=tree_el_jamon, 
                                          C=[".articulo"], 
                                          driver=self.driver, 
                                          elem_details=None, 
                                          num_pag=None)
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
    
    def test_generate_scraper_for_el_jamon(self):
        self.driver.get(self.generator.get_url())
        self.generator.generate()
        
    def generate_tree_for_el_jamon(self):
        
        result_tree = Tree()
        
        root = Node(selector=None, parent=None)
        result_tree.add(root)
        for i in range(11):
            child = Node(selector="#banner > div.wrapper-menus > div.contenido-menuCategorias > div > div > ul > li:nth-child(%d) > a.link-botcategoria > span" % (i+1), parent=root)
            result_tree.add(child)

        return result_tree
    
class ScrapersTestCaseRecursive(TestCase):
    
    def test_el_jamon_generated_scraper(self):
        recursive_scraper.scraper()
        
class ScrapersTestCaseStandard(TestCase):
    
    def test_el_jamon_generated_scraper(self):
        standard_scraper.scraper()