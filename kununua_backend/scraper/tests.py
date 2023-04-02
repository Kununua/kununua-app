from pathlib import Path
from django.test import TestCase
from .scraper_generator.model.Node import Node
from .scraper_generator.model.Tree import Tree
from .scraper_generator.ScraperGenerator import ScraperGenerator
from .utils.Timer import Timer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from django.conf import settings

from .scrapers import generated_scraper_recursive_template as recursive_scraper
from .scrapers import generated_scraper_standard_template as standard_scraper
from .scrapers.spain import scraper_el_jamon
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
                                          C=[".marca", ".nombre", ".precio", ".texto-porKilo", ".imgwrap > img", ".tachado"], 
                                          driver=self.driver, 
                                          elem_details=None, 
                                          num_pag=None,
                                          common_parent_selector=".articulo")
    
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
        
class ScraperElJamonTest(TestCase):
    
    def test_scraper_el_jamon(self):
        scraper_el_jamon.scraper()
        
class GeneratorMercadonaStandardCase(TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = False # Change to True if you want to run the scraper in headless mode
        self.driver = webdriver.Chrome(options=options)
        
        tree_mercadona = self.generate_tree_for_mercadona()
        
        self.generator = ScraperGenerator(url="https://www.mercadona.es", 
                                          country="Spain",
                                          tree=tree_mercadona, 
                                          C=[".product-cell__description-name", ".product-price__unit-price", "button > div.product-cell__info > div.product-format.product-format__size--cell > span:nth-child(2)", "button > div.product-cell__image-wrapper > img"], 
                                          driver=self.driver, 
                                          elem_details=None, 
                                          num_pag=None,
                                          common_parent_selector=".product-cell")
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
    
    def test_generate_scraper_for_mercadona(self):
        self.driver.get(self.generator.get_url())
        self.generator.generate()
        
    def generate_tree_for_mercadona(self):
        
        result_tree = Tree()
        
        root = Node(selector="#root > header > div.header__left > nav > a:nth-child(1)", parent=None)
        result_tree.add(root)
        for i in range(26):
            child = Node(selector="#root > div.grid-layout > div.grid-layout__sidebar > ul > li:nth-child(%d) > div > button > span > label" % (i+1), parent=root)
            result_tree.add(child)

        return result_tree
    
class GeneratorCarrefourStandardCase(TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = False # Change to True if you want to run the scraper in headless mode
        self.driver = webdriver.Chrome(options=options)
        
        tree_mercadona = self.generate_tree_for_carrefour()
        
        self.generator = ScraperGenerator(url="https://www.carrefour.es/", 
                                          country="Spain",
                                          tree=tree_mercadona, 
                                          C=[".product-card__price", ".product-card__price-per-unit", ".product-card__detail > h2 > a", ".product-card__image"], 
                                          driver=self.driver, 
                                          elem_details=None, 
                                          num_pag=None,
                                          common_parent_selector=".product-card")
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
    
    def test_generate_scraper_for_carrefour(self):
        self.driver.get(self.generator.get_url())
        self.generator.generate()
        
    def generate_tree_for_carrefour(self):
        
        result_tree = Tree()
        
        number_of_subcategories = {
            'Productos Frescos': 9,
            'La despensa': 8,
            'Congelados': 9,
            'Bebidas': 8,
            'Limplieza y Hogar': 12,
            'Perfumería e Higiene': 8,
            'Bebé': 5,
            'Mascotas': 5,
            'Parafarmacia': 8,
        }
        
        root = Node(selector="#app > div > main > div.home-view__main > div.page > div > div > div > div.hst-container-item.cms-distributor-cat > div > div > div > ul > li:nth-child(3) > div > div > a > div:nth-child(2) > h2", parent=None)
        result_tree.add(root)
        
        for i in range(3, 11):
            child = Node(selector="#app > div > nav > div:nth-child(2) > div.home-food-view__nav > div.horizontal-navigation > div > div.carousel__elements > div > div:nth-child(%d)" % (i), parent=root)
            result_tree.add(child)
            for j in range(list(number_of_subcategories.values())[i-3]):
                grandchild = Node(selector="#app > div > nav > div.plp-food-view__nav > div.horizontal-navigation.plp-food-view__nav-level--first > div.carousel.horizontal-navigation__second-level--parent > div.carousel__elements > div > div:nth-child(%d)" % (j+1), parent=child)
                result_tree.add(grandchild)

        return result_tree