from django.core.management.base import BaseCommand
from scraper.utils.Timer import Timer
from products.utils.cart_improvements_functions import improve_cart, improve_cart_optimization, improve_super_cart

import pandas as pd
import openpyxl

class Command(BaseCommand):
    help = 'Improve the given cart'

    def handle(self, *args, **options):
        
        cesta_prueba_1 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 2, "is_locked": False}, 
                          14565: {"quantity": 36, "is_locked": False}}
        
        cesta_prueba_2 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 1, "is_locked": False}, 
                          14565: {"quantity": 1, "is_locked": True}}
        
        cesta_prueba_3 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 2, "is_locked": False}, 
                          808: {"quantity": 3, "is_locked": False}, 
                          1048: {"quantity": 1, "is_locked": False}, 
                          2924: {"quantity": 7, "is_locked": False}, 
                          14565: {"quantity": 10, "is_locked": False}}
        
        cesta_prueba_4 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 2, "is_locked": False}, 
                          808: {"quantity": 3, "is_locked": False}, 
                          1048: {"quantity": 1, "is_locked": True}, 
                          2924: {"quantity": 7, "is_locked": False}, 
                          14565: {"quantity": 10, "is_locked": True}}
        
        cesta_prueba_5 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 1, "is_locked": False}, 
                          808: {"quantity": 1, "is_locked": False}, 
                          1048: {"quantity": 15, "is_locked": False}, 
                          2924: {"quantity": 3, "is_locked": False}, 
                          3064: {"quantity": 6, "is_locked": False},
                          3306: {"quantity": 2, "is_locked": False},
                          3644: {"quantity": 5, "is_locked": False},
                          3733: {"quantity": 4, "is_locked": False},
                          4729: {"quantity": 4, "is_locked": False},
                          4800: {"quantity": 1, "is_locked": False},
                          14565: {"quantity": 1, "is_locked": False}}
        
        cesta_prueba_6 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 1, "is_locked": False}, 
                          808: {"quantity": 1, "is_locked": True}, 
                          1048: {"quantity": 15, "is_locked": False}, 
                          2924: {"quantity": 3, "is_locked": True}, 
                          3064: {"quantity": 6, "is_locked": False},
                          3306: {"quantity": 2, "is_locked": False},
                          3644: {"quantity": 5, "is_locked": False},
                          3733: {"quantity": 4, "is_locked": False},
                          4729: {"quantity": 4, "is_locked": True},
                          4800: {"quantity": 1, "is_locked": False},
                          14565: {"quantity": 1, "is_locked": False}}
        
        cesta_prueba_7 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 25, "is_locked": False}, 
                          808: {"quantity": 1, "is_locked": False}, 
                          1048: {"quantity": 1, "is_locked": False}, 
                          2924: {"quantity": 3, "is_locked": False}, 
                          3064: {"quantity": 6, "is_locked": False},
                          3306: {"quantity": 2, "is_locked": False},
                          3644: {"quantity": 5, "is_locked": False},
                          3733: {"quantity": 1, "is_locked": False},
                          4729: {"quantity": 1, "is_locked": False},
                          4800: {"quantity": 10, "is_locked": False},
                          5000: {"quantity": 12, "is_locked": False},
                          7945: {"quantity": 2, "is_locked": False},
                          8012: {"quantity": 3, "is_locked": False},
                          9657: {"quantity": 3, "is_locked": False},
                          10087: {"quantity": 2, "is_locked": False},
                          11241: {"quantity": 4, "is_locked": False},
                          13982: {"quantity": 4, "is_locked": False},
                          14210: {"quantity": 2, "is_locked": False},
                          14565: {"quantity": 1, "is_locked": False}}
        
        cesta_prueba_8 = {91: {"quantity": 1, "is_locked": False}, 
                          153: {"quantity": 25, "is_locked": False}, 
                          808: {"quantity": 1, "is_locked": True}, 
                          1048: {"quantity": 1, "is_locked": False}, 
                          2924: {"quantity": 3, "is_locked": True}, 
                          3064: {"quantity": 6, "is_locked": False},
                          3306: {"quantity": 2, "is_locked": False},
                          3644: {"quantity": 5, "is_locked": False},
                          3733: {"quantity": 1, "is_locked": False},
                          4729: {"quantity": 1, "is_locked": True},
                          4800: {"quantity": 10, "is_locked": False},
                          5000: {"quantity": 12, "is_locked": False},
                          7945: {"quantity": 2, "is_locked": False},
                          8012: {"quantity": 3, "is_locked": True},
                          9657: {"quantity": 3, "is_locked": False},
                          10087: {"quantity": 2, "is_locked": False},
                          11241: {"quantity": 4, "is_locked": False},
                          13982: {"quantity": 4, "is_locked": False},
                          14210: {"quantity": 2, "is_locked": False},
                          14565: {"quantity": 1, "is_locked": False}}
        
        cestas = [cesta_prueba_1, cesta_prueba_2, cesta_prueba_3, cesta_prueba_4, cesta_prueba_5, cesta_prueba_6, cesta_prueba_7, cesta_prueba_8]

        pandas_df_results = []

        for i in range(len(cestas)):

            cesta = cestas[i]
        
            timer_normal = Timer()
            timer_optimizacion = Timer()
            timer_super_cart = Timer()
        
            timer_normal.start()
            result1 = improve_cart(cesta, 2)
            timer_normal.stop()

            #print(result1)

            timer_optimizacion.start()
            # Sintaxis de variables: x_{id_producto}_{id_supermercado}_{id_variable}
            result2 = improve_cart_optimization(cesta)
            timer_optimizacion.stop()

            # for variable in result2:
            #     print(variable, result2[variable].varValue)

            timer_super_cart.start()
            result3 = improve_super_cart(cesta, 2)
            timer_super_cart.stop()

            # total_cost = result3.get_objective("Total_Cost")
            # variables_x = result3.get_variable("x")
            # variables_y = result3.get_variable("y")

            # print("Total Cost = ", total_cost.get().value())
            # print("---------------------------")
            # print("VARIABLES X")
            # for variable in variables_x:
            #     print(str(variable[0]) + ":" + str(variable[1].value()))
            # print("---------------------------")
            # print("VARIABLES Y")
            # for variable in variables_y:
            #     print(str(variable[0]) + ":" + str(variable[1].value()))

            # print(f"----------------------------- PRUEBA {i} -----------------------------")
            
            # print("Normal: ", timer_normal.get_time())
            # print("Optimizacion: ", timer_optimizacion.get_time())
            # print("Super Optimizacion: ", timer_super_cart.get_time())
            
            # print("--------------------------------------------------------------------")

            pandas_df_results.append([i, timer_normal.get_time()*1000, timer_optimizacion.get_time()*1000, timer_super_cart.get_time()*1000])

        df = pd.DataFrame(pandas_df_results, columns=["Nº Prueba", "Normal (ms)", "Optimizacion (ms)", "Super Optimizacion (ms)"])

        df.to_excel("./resultados.xlsx", index=False)
        #df.to_csv("./resultadosCSV.csv", index=False)