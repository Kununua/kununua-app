import graphene, jwt
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductEntry, Cart
from .types import ProductType, CartType

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
  
class AddEntryToCartMutation(graphene.Mutation):
  
  class Input:
    user_token = graphene.String(required=True)
    product_id = graphene.Int(required=True)
    amount = graphene.Int(required=True)
    
  entry = graphene.Field(CartType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    
    user_token = kwargs.get('user_token', '')
    product_id = kwargs.get('product_id', 0)
    amount = kwargs.get('amount', 0)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if product_id != 0:
      selected_product = Product.objects.get(pk=product_id)
    else:
      raise ValueError(_("Invalid product"))
    
    if amount <= 0:
      raise ValueError(_("The amount must be greater than 0"))
    
    user_cart = Cart.objects.get(user__username=user['username'])
    
    entry = ProductEntry.objects.create(product=selected_product, quantity=amount, cart=user_cart, list=None, is_list_product=False)
    
    return AddEntryToCartMutation(entry=entry)

class ProductsMutation(graphene.ObjectType):
  add_image_to_product = AddImageToProductMutation.Field()
  add_entry_to_cart = AddEntryToCartMutation.Field()