from django.core.management.base import BaseCommand
from scraper.utils.Timer import Timer
from products.utils.cart_improvements_functions import improve_cart, improve_cart_optimization, translate_cart_improvement_result, improve_super_cart

class Command(BaseCommand):
    help = 'Improve the given cart'

    def handle(self, *args, **options):
        
        cesta_prueba_1 = {91: {"quantity": 1, "is_locked": False}, 153: {"quantity": 1, "is_locked": False}, 494: {"quantity": 6, "is_locked": False}}
        cesta_prueba_2 = {91: {"quantity": 1, "is_locked": False}, 153: {"quantity": 1, "is_locked": False}, 494: {"quantity": 1, "is_locked": True}}
        
        # PRUEBA 1
        
        timer_normal = Timer()
        timer_optimizacion = Timer()
        timer_super_cart = Timer()
        
        timer_normal.start()
        result1 = improve_cart(cesta_prueba_1, 1)
        print(result1)
        timer_normal.stop()
        timer_optimizacion.start()
        # Sintaxis de variables: x_{id_producto}_{id_supermercado}_{id_variable}
        result2 = improve_cart_optimization(cesta_prueba_1)
        for variable in result2:
            print(variable, result2[variable].varValue)
        timer_optimizacion.stop()
        timer_super_cart.start()
        result3 = improve_super_cart(cesta_prueba_1, 1)
        timer_super_cart.stop()
        

        print("----------------------------- PRUEBA 1 -----------------------------")
        
        print("Normal: ", timer_normal.get_time())
        print("Optimizacion: ", timer_optimizacion.get_time())
        print("Super Optimizacion: ", timer_super_cart.get_time())
        
        print("--------------------------------------------------------------------")
        
        # PRUEBA 2
        
        timer_normal = Timer()
        timer_optimizacion = Timer()
        timer_super_cart = Timer()
        
        timer_normal.start()
        result1 = improve_cart(cesta_prueba_2, 2)    
        timer_normal.stop()
        timer_optimizacion.start()
        # Sintaxis de variables: x_{id_producto}_{id_supermercado}_{id_variable}
        result2 = improve_cart_optimization(cesta_prueba_2)
        timer_optimizacion.stop()
        timer_super_cart.start()
        result3 = improve_super_cart(cesta_prueba_2, 2)
        timer_super_cart.stop()
        
        print("----------------------------- PRUEBA 2 -----------------------------")
        
        print("Normal: ", timer_normal.get_time())
        print("Optimizacion: ", timer_optimizacion.get_time())
        print("Super Optimizacion: ", timer_super_cart.get_time())
        
        print("--------------------------------------------------------------------")