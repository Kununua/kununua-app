from django.core.management.base import BaseCommand
from data.synonyms import CategoryFinder
from products.models import Category


class Command(BaseCommand):
    help = 'Find the most similar category for the given product and category'

    def handle(self, *args, **options):
        if Category.objects.count() != 16:
            Category.objects.all().delete()
            Category.objects.create(name="Carnicería")
            Category.objects.create(name="Charcutería")
            Category.objects.create(name="Lácteos")
            Category.objects.create(name="Despensa")
            Category.objects.create(name="Frutas y verduras")
            Category.objects.create(name="Bebidas")
            Category.objects.create(name="Congelados")
            Category.objects.create(name="Panadería y dulces")
            Category.objects.create(name="Limpieza y hogar")
            Category.objects.create(name="Bebés")
            Category.objects.create(name="Perfumería e higiene")
            Category.objects.create(name="Del mar")
            Category.objects.create(name="Bodega")
            Category.objects.create(name="Parafarmacia")
            Category.objects.create(name="Mascotas")
            Category.objects.create(name="Platos preparados")
        
        cat = CategoryFinder()
        print(cat.find_category("Pizza barbacoa Hacendado", "Pizzas y platos preparados", "es"))
        