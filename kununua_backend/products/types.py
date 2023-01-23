import graphene, base64
from .models import Product
from graphene_django.types import DjangoObjectType
from .serializers import ProductSerializer

class ProductType(DjangoObjectType):
  class Meta:
    model = Product
    
class ProductQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
    
    with open(product.image.url[1:], "rb") as img:
      
        encoded_image = base64.b64encode(bytes(img.read()))
      
        product.image = encoded_image.decode("utf-8")
  
    return product