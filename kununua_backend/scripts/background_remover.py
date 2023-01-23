# Program name: remove-background.py
# imports
from rembg import remove 
from PIL import Image 
# Using Pillow to open the input image
input_image = Image.open("/Users/alejandro/Desktop/Proyectos/Universidad/kununua-app/django_api/scripts/pechuga.jpg")
output_image = remove(input_image)
output_image.save("/Users/alejandro/Desktop/Proyectos/Universidad/kununua-app/django_api/scripts/ejemplo-trans.png")
print('Transformation Done')