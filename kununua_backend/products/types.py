import graphene, base64
from .models import Product, Supermarket, Category, Rating, List, Cart, ProductEntry, Price, Brand
from graphene_django.types import DjangoObjectType
from .utils.image_coder import encode_image
from django.db.models import Avg

class ProductType(DjangoObjectType):
  class Meta:
    model = Product
    
  average_rating = graphene.Float()
  
  @staticmethod
  def resolve_average_rating(root, info, **kwargs):
    return Rating.objects.filter(product=root).aggregate(Avg('rating'))['rating__avg']

class FilterType(graphene.ObjectType):
  key = graphene.String()
  options = graphene.List(graphene.String)
  
class ProductFilterType(graphene.ObjectType):
  products = graphene.List(ProductType)
  filters = graphene.List(FilterType)
  
class PriceType(DjangoObjectType):
  class Meta:
    model = Price
  
class BrandType(DjangoObjectType):
  class Meta:
    model = Brand
    
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