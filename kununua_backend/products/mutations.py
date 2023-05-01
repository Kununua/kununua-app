import graphene, jwt
from django.utils.translation import gettext_lazy as _
from .models import Price, Product, ProductEntry, Cart
from .types import ProductType, CartType, ProductEntryType

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
    price_id = graphene.Int(required=True)
    amount = graphene.Int(required=True)
    
  entry = graphene.Field(ProductEntryType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    
    user_token = kwargs.get('user_token', '')
    price_id = kwargs.get('price_id', 0)
    amount = kwargs.get('amount', 0)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if price_id != 0:
      selected_price = Price.objects.get(pk=price_id)
    else:
      raise ValueError(_("Invalid product"))
    
    if amount <= 0:
      raise ValueError(_("The amount must be greater than 0"))
    
    existing_entry = ProductEntry.objects.filter(product_price=selected_price, cart__user__username=user['username'])
    
    if len(existing_entry) == 1:
      existing_entry[0].quantity += amount
      existing_entry[0].save()
      return AddEntryToCartMutation(entry=existing_entry[0])
    elif len(existing_entry) == 0:
      user_cart = Cart.objects.get(user__username=user['username'])
      entry = ProductEntry.objects.create(product_price=selected_price, quantity=amount, cart=user_cart, list=None, is_list_product=False)
      return AddEntryToCartMutation(entry=entry)
    else:
      raise ValueError(_("There are more than one entry for this product in the cart"))
    
class EditCartEntryMutation(graphene.Mutation):
  
  class Input:
    user_token = graphene.String(required=True)
    price_id = graphene.Int(required=True)
    amount = graphene.Int(required=True)
    
  entry = graphene.Field(ProductEntryType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    
    user_token = kwargs.get('user_token', '')
    price_id = kwargs.get('price_id', 0)
    amount = kwargs.get('amount', 0)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if price_id != 0:
      selected_price = Price.objects.get(pk=price_id)
    else:
      raise ValueError(_("Invalid product"))
    
    if amount < 0:
      raise ValueError(_("The amount must be greater than 0"))
    
    existing_entry = ProductEntry.objects.filter(product_price=selected_price, cart__user__username=user['username'])
    
    if len(existing_entry) == 1:
      if amount == 0:
        existing_entry[0].delete()
        return EditCartEntryMutation(entry=None)
      else:
        existing_entry[0].quantity = amount
        existing_entry[0].save()
        return EditCartEntryMutation(entry=existing_entry[0])
    else:
      raise ValueError(_("There is no entry for this product in the cart"))

class ProductsMutation(graphene.ObjectType):
  add_image_to_product = AddImageToProductMutation.Field()
  add_entry_to_cart = AddEntryToCartMutation.Field()
  edit_cart_entry = EditCartEntryMutation.Field()