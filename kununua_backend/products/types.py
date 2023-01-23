import graphene, base64
from .models import Product, Supermarket, Category, Rating, List, Cart, ProductEntry
from graphene_django.types import DjangoObjectType
from location.types import CountryType, CurrencyType

class ProductType(DjangoObjectType):
  class Meta:
    model = Product
    
class SupermarketType(DjangoObjectType):
  class Meta:
    model = Supermarket
    
class CategoryType(DjangoObjectType):
  class Meta:
    model = Category

class RatingType(DjangoObjectType):
  class Meta:
    model = Rating
    
class ListType(DjangoObjectType):
  class Meta:
    model = List

class CartType(DjangoObjectType):
  class Meta:
    model = Cart
    
class ProductEntryType(DjangoObjectType):
  class Meta:
    model = ProductEntry
    
class ProductsQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
    
    with open(product.image.url[1:], "rb") as img:
      
        encoded_image = base64.b64encode(bytes(img.read()))
      
        product.image = encoded_image.decode("utf-8")
  
    return product