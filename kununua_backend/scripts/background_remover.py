# Program name: remove-background.py
# imports
from rembg import remove 
from PIL import Image 
# Using Pillow to open the input image
input_image = Image.open("/Users/alejandro/Desktop/Proyectos/Universidad/kununua-app/kununua_backend/scripts/pechuga-de-pavo-carrefour.jpg")
output_image = remove(input_image)
output_image.save("/Users/alejandro/Desktop/Proyectos/Universidad/kununua-app/kununua_backend/scripts/ejemplo-trans.png")
print('Transformation Done')