import math
import re
from django.core.management.base import BaseCommand
import stanza, itertools

DISTANCE_UNITS = ["km", "m", "dm", "cm", "mm"]
VOLUME_UNITS = ["kl", "l", "dl", "cl", "ml"]
MASS_UNITS = ["kg", "g", "dg", "cg", "mg"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", "."]
PRUEBAS = """carrefour barritas para periquitos con frutas 2x30g
1,29 €/ud
1.29
vitakraft barritas para periquitos de albaricoque & higo
24,83 €/kg
1.49
barritas fortalecedor para canarios vitakraft 2 uds
0,74 €/ud
1.49
menú provita agapornis 750 gr vitakraft
7,87 €/kg
5.9
tetra reptomin comida para tortugas acuáticas 1l/220g
87,68 €/kg
7.59
pienso de salmón con avena para perro purina adulto beyond 3 kg
5,92 €/kg
17.75
pienso de buey para perro purina beyond 1,2 kg
8,46 €/kg
10.15
toallitas higiénicas perro 40 pcs
0,10 €/ud
3.95
pelota de tenis para perros vitakraft
2,19 €/ud
2.19
biberón con tetina silicona + 3 meses suavinex 270 ml
10,75 €/ud
10.75
biberón con tetina de látex anatómica flujo medio 0-6 meses suavinex 270 ml
8,85 €/ud
8.85
bastones de zanahoria para conejos enanos vitakraft  50grs
31,40 €/kg
1.57"""

UNIT_TRANSLATIONS = {
    'gr': 'g',
    'grs': 'g',
    'gramo': 'g',
    'gramos': 'g',
    'kilo': 'kg',
    'kilogramo': 'kg',
    'kilogramos': 'kg',
    'litro': 'l',
    'litros': 'l',
    'mililitro': 'ml',
    'mililitros': 'ml',
    'centilitro': 'cl',
    'centilitros': 'cl',
    'kgs': 'kg',
    'kilos': 'kg',
    'metros': 'm',
    'metro': 'm',
    'centimetros': 'cm',
    'centimetro': 'cm',
    'milimetros': 'mm',
    'milimetro': 'mm',
    'centímetros': 'cm',
    'centímetro': 'cm',
    'milímetros': 'mm',
    'milímetro': 'mm',
}

class Command(BaseCommand):
    help = 'Populates the database with the supported brands'

    def handle(self, *args, **options):
        
        def get_unit_family(unit):
            if unit in DISTANCE_UNITS:
                return DISTANCE_UNITS
            elif unit in VOLUME_UNITS:
                return VOLUME_UNITS
            elif unit in MASS_UNITS:
                return MASS_UNITS
            else:
                return None
        
        price = 1.90
        weight = "1000GR"
        
        weight_unit = UNIT_TRANSLATIONS[re.sub('[0-9]+', '', weight.lower())]
        weight_value = float(re.sub('[a-z]+', '', weight.lower()))
        
        print(weight_unit)
        print(weight_value)
        
        selected_unit_family = get_unit_family(weight_unit)
        
        print(selected_unit_family)
        
        unit_price_value = price/weight_value
        
        if weight_unit in selected_unit_family[0] and math.floor(unit_price_value) > 100:
            
            weight_unit = selected_unit_family[1]
            unit_price_value = unit_price_value/1000
            
        elif weight_unit in selected_unit_family[1] and float('%.2f'%unit_price_value) == 0 :
            
            print(unit_price_value)
            
            weight_unit = selected_unit_family[0]
            unit_price_value = unit_price_value*1000
            
        print(str(unit_price_value) + " €/" + weight_unit)
        
        # def get_unit_family(unit):
        #     if unit in DISTANCE_UNITS:
        #         return DISTANCE_UNITS
        #     elif unit in VOLUME_UNITS:
        #         return VOLUME_UNITS
        #     elif unit in MASS_UNITS:
        #         return MASS_UNITS
        #     else:
        #         return None
        
        # splitted_pruebas = PRUEBAS.split("\n")
        
        # i = 0
        
        # while i < len(splitted_pruebas):
        #     phrase = splitted_pruebas[i]
        #     price = float(splitted_pruebas[i+2])
        #     unit_price = splitted_pruebas[i+1]
        #     weight_unit = unit_price.split("/")[1].strip()
        #     for number in NUMBERS:
        #             weight_unit = weight_unit.replace(number, "")
        #     round_to = 1 if "ud" not in weight_unit and "unidad" not in weight_unit else 0
            
        #     weight = "Error"
            
        #     numeros = []
                    
        #     if weight == "Error":
                
        #         unit_price_value = float(unit_price.split("/")[0].replace(",", ".").replace("€", "").strip())
                
        #         weight_value = str(price/unit_price_value)
                
        #         if weight_value.startswith("0."):
                    
        #             weight_value_float = float(weight_value)
                    
        #             index = get_unit_family(weight_unit).index(weight_unit)
                    
        #             if index == 0:
        #                 weight_value_float = weight_value_float*1000
        #             elif index == 1:
        #                 continue
        #             else:
        #                 parsing_factor = index-1
        #                 weight_value_float = weight_value_float/(10**parsing_factor)
                    
        #             weight = str(round(weight_value_float, round_to)) + get_unit_family(weight_unit)[1]
                
        #         elif "." in weight_value:
        #             weight = str(round(float(weight_value), round_to)) + weight_unit
        #         else:
        #             weight = str(round(float(weight_value), round_to)) + weight_unit
                  
        #     phrase = phrase.replace(weight, "")
              
        #     if "/" in weight:
        #         weight = weight.split("/")[1][:-1]
                    
        #     i += 3
        #     print(f"Numeros: {numeros}")
        #     print(f"Producto: {phrase} | Peso: {weight}")
        #     print("---------------------------------")