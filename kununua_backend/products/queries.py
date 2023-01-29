import graphene, jwt
from django.utils.translation import gettext_lazy as _
from .types import ProductType, CategoryType, ProductEntryType
from authentication.models import KununuaUser
from location.types import CountryType
from .models import Product, Category, Cart, ProductEntry
from .utils.image_coder import encode_image


class ProductsQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())
  get_products_by_category = graphene.List(ProductType, category=graphene.String())
  get_products_with_offer = graphene.List(ProductType)

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
  
    return product
  
  def resolve_get_products_by_category(self, info, category):
    
    products = Product.objects.filter(category__name=category)[:20]
    
    # TODO: Añadir paginación, retraso por codificacion de imagenes, orden, etc.
    
    return products
  
  def resolve_get_products_with_offer(self, info):
    
    products = Product.objects.filter(offer_price__isnull=False)[:20]
    
    return products
  
class CategoriesQuery(object):
  
  get_all_categories = graphene.List(CategoryType)
  
  def resolve_get_all_categories(self, info):
    return Category.objects.all().order_by('name')
  
class CartQuery(object):
  
  get_cart = graphene.List(ProductEntryType, user_token=graphene.String())
  
  def resolve_get_cart(self, info, user_token):
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    user = KununuaUser.objects.get(username=user['username'])
    
    cart = Cart.objects.get(user=user)
    
    return ProductEntry.objects.filter(cart=cart)