model_name = "../scripts/output/kununua-2023-06-28_08-29-25"

from sentence_transformers import CrossEncoder

model = CrossEncoder(model_name)

print("Modelo cargado.")

scores1 = model.predict([('Comida para perros con atun, cebolla y arroz', 'Eureka')])
scores2 = model.predict([('Comida para perros con atun, cebolla y arroz', 'Comida para gatos con atun, cebolla y arroz')])
scores3 = model.predict([('Refresco naranja botella Fanta', 'Refresco Fanta Limón')])
scores4 = model.predict([('Refresco Coca-Cola, 1.5L', 'Refresco Coca-Cola, 2L')])
scores5 = model.predict([('Refresco Coca-Cola, 500ml', 'Refresco Coca-Cola, 2L')])

print("Similarities1: " + str(scores1))
print("Similarities2: " + str(scores2))
print("Similarities3: " + str(scores3))
print("Similarities4: " + str(scores4))
print("Similarities5: " + str(scores5))