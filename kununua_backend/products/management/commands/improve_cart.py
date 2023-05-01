import itertools
from products.models import Price, Product, Supermarket
from django.core.management.base import BaseCommand
from django.db.models import Min, Count, F, Case, When, Value, DecimalField

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD
from scraper.utils.Timer import Timer
import numpy as np
from scipy.optimize import minimize

class Command(BaseCommand):
    help = 'Improve the given cart'

    def handle(self, *args, **options):
        
        def repeated_locked_products(locked_products):
            
            readed_products = []
            
            for product in locked_products:
                
                if product.product.pk in readed_products:
                    return True
                
                readed_products.append(product.product.pk)
                
            return False
        
        def improve_cart(items_in_cart, max_supermarkets, allowed_supermarkets=None, not_improved_mem=None):
            
            # Separate items that need to be optimiced from those that doesn't
            # Also define the number of product to improve in order to check that the optimization result includes all the products.
            item_to_upgrade_ids = [id for id in items_in_cart.keys() if not items_in_cart[id]["is_locked"]]
            items_to_not_upgrade_ids = set(items_in_cart)-set(item_to_upgrade_ids)
            number_of_products_to_improve = Price.objects.filter(pk__in=items_in_cart).values('product').distinct().count()
            
            # Check if the cart contains repeated locked products 
            # (this is two prices of the same product locked in the cart)
            if items_to_not_upgrade_ids:
                locked_products = Price.objects.filter(pk__in=items_to_not_upgrade_ids)
                
                if repeated_locked_products(locked_products):
                    raise ValueError('The cart contains repeated products')
            else:
                locked_products = []
            
            # Save the ids of the products that are already optimiced (locked products)
            optimiced_ids = [p.product.pk for p in locked_products]
            
            improved_products = []
            not_improved_products = []
            
            # Enters here if there are no supermarkets on which optimize the cart.
            # If allowed_supermarkets is defined (only happens when the recursion starts), sets that list as current supermarkets
            # current_supermarket is a variable that control on how many supermarkets the cart is being divided.
            # It's also used to determine if the products can be optimized for the given allowed_supermarkets.
            if not allowed_supermarkets:
                current_supermarkets = set(map(lambda p: (p.supermarket.name, p.supermarket.zipcode), locked_products))
            
                if len(current_supermarkets) > max_supermarkets:
                    raise ValueError('The cart already exceed the maximum number of supermarkets')
            else:
                current_supermarkets = allowed_supermarkets
            
            # Save the quantity that exists on the cart for each product
            products_to_optimice = {}
            
            for item_id in item_to_upgrade_ids:
            
                item_product = Product.objects.get(price__pk=item_id)
                
                products_to_optimice[item_product.pk] = items_in_cart[item_id]["quantity"]
            
            # Get the Price objects that optimice the cart.
            # If allowed_supermarkets is given, the query is forced to find the min price only on those supermarkets
            # This first variable, product_multipliers, is used to multiply the price of each product by the quantity that exists on the cart.
            product_multipliers = product_multipliers = Case(
                *[When(product__pk=pk, then=Value(multiplier, output_field=DecimalField())) for pk, multiplier in products_to_optimice.items()]
            )
            
            if not allowed_supermarkets:
                optimal_prices = Price.objects.filter(product__in=products_to_optimice) \
                                                .values('product') \
                                                .annotate(min_price=Min(F('price')*product_multipliers)) \
                                                .order_by('min_price')
            else:
                optimal_prices = Price.objects.filter(product__in=products_to_optimice, 
                                                      supermarket__name__in=[s[0] for s in current_supermarkets],
                                                      supermarket__zipcode__in=[s[1] for s in current_supermarkets]
                                                      ) \
                                                .values('product') \
                                                .annotate(min_price=Min(F('price')*product_multipliers)) \
                                                .order_by('min_price')
            
            # Once we have the optimal prices, we check if the cart can be optimized that way, or exceeds the max_supermarkets condition.
            # All the products that cannot be added because the number of supermarkets is exceeded are saved in not_improved_products.
            for product in list(optimal_prices):
                
                if product['product'] in optimiced_ids:
                    continue
                
                options = Price.objects.filter(product__pk=product['product'], price=product['min_price']/products_to_optimice[product['product']])

                for option in options:
                    
                    if (option.supermarket.name, option.supermarket.zipcode) in current_supermarkets:
                        option.price = option.price * products_to_optimice[product['product']]
                        improved_products.append(option)
                        optimiced_ids.append(option.pk)
                        break
                else:
                    option = options[0]
                    option.price = option.price * products_to_optimice[product['product']]
                    if len(current_supermarkets) < max_supermarkets:
                        improved_products.append(option)
                        current_supermarkets.add((option.supermarket.name, option.supermarket.zipcode))
                    else:
                        not_improved_products.append(options[0])
            
            # If there are not_improved_products, we run a recursion with the different possible supermarkets combinations
            # and then, take the one that minimize the total price.
            if len(not_improved_products) > 0:
                
                if not_improved_products == not_improved_mem:
                    raise ArithmeticError("It's not possible to improve this cart")
                else:
                    
                    all_supermarkets = Supermarket.objects.all()
                    possible_combinations = list(itertools.combinations(all_supermarkets, max_supermarkets))
                    possible_combinations = list(map(lambda s: set(map(lambda x: (x.name, x.zipcode), s)), possible_combinations))
                    
                    possible_results = {}
                    
                    for i in range(len(possible_combinations)):
                        try:
                            possible_results[i] = improve_cart(items_in_cart, max_supermarkets, allowed_supermarkets=possible_combinations[i], not_improved_mem=not_improved_products)
                        except ArithmeticError:
                            possible_results[i] = None
                            
                    min_value = min(possible_results, key=lambda x: sum([p.price for p in possible_results[x]]) if possible_results[x] != None else 10000000)
                    
                    return possible_results[min_value]
            
            # In other case, we return the optimized cart.
            # Have in mind that the function is not meant to return Price objects with the actual price. 
            # This attribute is multiplied by the quantity of each products in the result of this function.
            
            cart_to_be_returned = list(improved_products) + list(locked_products)
            
            if len(cart_to_be_returned) != number_of_products_to_improve:
                raise ArithmeticError("It's not possible to improve this cart")
            
            return cart_to_be_returned
            
        def improve_cart_optimization(items_in_cart):
            
            products_to_optimice_ids = [p['product'] for p in Price.objects.filter(pk__in=items_in_cart.keys()).values('product').distinct()]
            items_to_upgrade_ids = [id for id in items_in_cart.keys() if not items_in_cart[id]["is_locked"]]
            items_to_not_upgrade_ids = set(items_in_cart)-set(items_to_upgrade_ids)
            possible_prices = Price.objects.filter(product__in=products_to_optimice_ids).values('product').annotate(dcount=Count('supermarket'))
            
            if items_to_not_upgrade_ids:
            
                locked_products = Price.objects.filter(pk__in=items_to_not_upgrade_ids)
                
                if repeated_locked_products(locked_products):
                    raise ValueError('The cart contains repeated products')
            
            grouped_prices = {}
            
            for price in possible_prices:
                grouped_prices[price['product']] = Price.objects.filter(product=price['product']).values('supermarket', 'price')
                
            products_to_optimice = {}
            
            for item_id in items_in_cart:
            
                item_product = Product.objects.get(price__pk=item_id)
                
                products_to_optimice[item_product.pk] = items_in_cart[item_id]["quantity"]
            
            # Creating the LP problem
            
            cart_optimization_problem = LpProblem("CART_OPTIMIZATION", LpMinimize)
            
            # Defining LP variables
            
            variable_names = []
            
            for id in products_to_optimice_ids:
                
                product_prices = grouped_prices[id]
                
                for i in range(len(product_prices)):
                    variable_names.append(str(id)+'_'+str(product_prices[i]['supermarket'])+'_'+str(i+1))
                
            lp_variables = LpVariable.dicts('x', variable_names, cat='Binary')
            
            # Objective function & restrictions
            
            current_prices = []
            grouped_lp_variables = {}
            locked_variables = []
            
            for i in range(len(products_to_optimice_ids)): 
                for j in range(len(grouped_prices[products_to_optimice_ids[i]])):
                    
                    # Objective function data build
                    
                    price = grouped_prices[products_to_optimice_ids[i]][j]['price']
                    variable_supermarket_name = str(grouped_prices[products_to_optimice_ids[i]][j]['supermarket'])
                    variable_name = str(products_to_optimice_ids[i])+'_'+variable_supermarket_name+'_'+str(j+1)
                    product_id = variable_name.split("_")[0]
                    
                    current_prices.append(price*lp_variables[variable_name]*products_to_optimice[int(product_id)])
                    
                    # Restriction one price per product data build
                    
                    if product_id in grouped_lp_variables.keys():
                        grouped_lp_variables[product_id].append(variable_name)
                    else:
                        grouped_lp_variables[product_id] = [variable_name]
                    
                    supermarket_id = variable_name.split("_")[-1]
                        
                    # Restriction locked products data build

                    supermarket_prices = Price.objects.filter(product__pk=int(product_id), supermarket__pk=int(supermarket_id))
                    
                    for price in supermarket_prices:
                        if price.pk in items_to_not_upgrade_ids:
                            locked_variables.append(variable_name)
            
            # Objective function
            cart_optimization_problem += lpSum(current_prices)
            
            # Restrictions
            
            for variable in locked_variables:
                cart_optimization_problem += lp_variables[variable] == 1
            
            for key in grouped_lp_variables.keys():
                
                one_price_per_product_restriction_variables = []
                
                for variable in grouped_lp_variables[key]:
                    one_price_per_product_restriction_variables.append(lp_variables[variable])
                
                cart_optimization_problem += lpSum(one_price_per_product_restriction_variables) == 1
            
            # Solving the problem and printing the results
            
            cart_optimization_problem.solve(PULP_CBC_CMD(msg=False))
            
            # for variable in lp_variables:
            #     print(variable, lp_variables[variable].varValue)
                
        def translate_cart_improvement_result(result, cesta):
            
            result_dict = {}
            
            for item in result:
                
                db_price = Price.objects.get(pk=item.pk)
                
                result_dict[item.product.name] = db_price.price
                
            return result_dict
        
        cesta_prueba_1 = {1: {"quantity": 200, "is_locked": False}, 3: {"quantity": 1, "is_locked": False}, 46: {"quantity": 1, "is_locked": False}}
        cesta_prueba_2 = {1: {"quantity": 1, "is_locked": False}, 3: {"quantity": 1, "is_locked": False}, 46: {"quantity": 1, "is_locked": True}}
        
        # PRUEBA 1
        
        timer_normal = Timer()
        timer_optimizacion = Timer()
        
        timer_normal.start()
        result1 = improve_cart(cesta_prueba_1, 1)
        print(translate_cart_improvement_result(result1, cesta_prueba_1))
        timer_normal.stop()
        timer_optimizacion.start()
        # Sintaxis de variables: x_{id_producto}_{id_supermercado}_{id_variable}
        result2 = improve_cart_optimization(cesta_prueba_1)
        timer_optimizacion.stop()

        print("----------------------------- PRUEBA 1 -----------------------------")
        
        print("Normal: ", timer_normal.get_time())
        print("Optimizacion: ", timer_optimizacion.get_time())
        
        print("--------------------------------------------------------------------")
        
        # PRUEBA 2
        
        timer_normal = Timer()
        timer_optimizacion = Timer()
        
        timer_normal.start()
        result1 = improve_cart(cesta_prueba_2, 2)    
        timer_normal.stop()
        timer_optimizacion.start()
        # Sintaxis de variables: x_{id_producto}_{id_supermercado}_{id_variable}
        result2 = improve_cart_optimization(cesta_prueba_2)
        timer_optimizacion.stop()
        
        print("----------------------------- PRUEBA 2 -----------------------------")
        
        print("Normal: ", timer_normal.get_time())
        print("Optimizacion: ", timer_optimizacion.get_time())
        
        print("--------------------------------------------------------------------")