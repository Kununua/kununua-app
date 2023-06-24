sentences = [
    "Patatas pringles sabor menta",
    "Patatas pringles sabor chuche",
    "Pringles de menta",
    "Patatas lays campesinas"
]

model_name = "cross-encoder/quora-distilroberta-base"

from sentence_transformers import CrossEncoder

model = CrossEncoder(model_name)

print("Modelo cargado.")

scores = model.predict([('Comida para perros con atun, cebolla y arroz', 'Comida para perros con atun, cebolla y arroz'), ('Patatas pringles sabor menta', 'Patatas pringles sabor chuche'), ('Comida para perros con atun, cebolla y arroz', 'Comida para perros con atun, cebolla y arroz'), ('Patatas pringles sabor menta', 'Patatas pringles sabor chuche'), ('Comida para perros con atun, cebolla y arroz', 'Comida para perros con atun, cebolla y arroz'), ('Patatas pringles sabor menta', 'Patatas pringles sabor chuche'), ('Comida para perros con atun, cebolla y arroz', 'Comida para perros con atun, cebolla y arroz'), ('Patatas pringles sabor menta', 'Patatas pringles sabor chuche'), ('Comida para perros con atun, cebolla y arroz', 'Comida para perros con atun, cebolla y arroz'), ('Patatas pringles sabor menta', 'Patatas pringles sabor chuche')])

print("Similarities: " + str(scores))