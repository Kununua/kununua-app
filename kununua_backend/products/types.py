import graphene, base64
from .models import Product, Supermarket, Category, Rating, List, Cart, ProductEntry
from graphene_django.types import DjangoObjectType
from .utils.image_coder import encode_image

class ProductType(DjangoObjectType):
  class Meta:
    model = Product
    
  image_encoded = graphene.String()
  
  def resolve_image_encoded(self, info):
    return encode_image(self.image.url)
    
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