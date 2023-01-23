import graphene
from django.utils.translation import gettext_lazy as _
from .models import Product
from .types import ProductType

class AddImageToProductMutation(graphene.Mutation):

  class Input:
    id = graphene.Int(required=True)

  product = graphene.Field(ProductType)

  @staticmethod
  def mutate(root, info, **kwargs):
    id = kwargs.get('id', 0)
    
    selected_product = Product.objects.get(pk=id)

    with open("products/pechua-de-pavo-carrefour.png", "rb") as img:

        selected_product.image.save("pechuga-de-pavo-carrefour.png", img, save=True)
    
    return AddImageToProductMutation(product=selected_product)

class ProductsMutation(graphene.ObjectType):
  add_image_to_product = AddImageToProductMutation.Field()