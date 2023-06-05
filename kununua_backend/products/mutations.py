import graphene, jwt
from django.utils.translation import gettext_lazy as _
from .models import Price, Product, ProductEntry, Cart, Supermarket, List, KununuaUser
from .types import ProductType, ListType, ProductEntryType
from products.utils.cart_improvements_functions import improve_cart, improve_cart_optimization, translate_cart_improvement_result, translate_cart_optimization_improvement_result

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
    amount = graphene.Int(required=False)
    locked = graphene.Boolean(required=False)
    
  entry = graphene.Field(ProductEntryType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    
    user_token = kwargs.get('user_token', '')
    price_id = kwargs.get('price_id', 0)
    amount = kwargs.get('amount', None)
    locked = kwargs.get('locked', None)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if price_id != 0:
      selected_price = Price.objects.get(pk=price_id)
    else:
      raise ValueError(_("Invalid product"))
    
    if amount and amount < 0:
      raise ValueError(_("The amount must be greater than 0"))
    
    existing_entry = ProductEntry.objects.filter(product_price=selected_price, cart__user__username=user['username'])
    
    if len(existing_entry) == 1:
      if amount:
        if amount == 0:
          existing_entry[0].delete()
          return EditCartEntryMutation(entry=None)
        else:
          existing_entry[0].quantity = amount
          existing_entry[0].save()
          return EditCartEntryMutation(entry=existing_entry[0])
        
      if locked is not None:
        existing_entry[0].locked = locked
        existing_entry[0].save()
        return EditCartEntryMutation(entry=existing_entry[0])
    else:
      raise ValueError(_("There is no entry for this product in the cart"))
    
class UpgradeCartMutation(graphene.Mutation):
  
  class Input:
    user_token = graphene.String(required=True)
    max_supermarkets = graphene.Int(required=False)
    
  entry = graphene.List(ProductEntryType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    
    user_token = kwargs.get('user_token', '')
    max_supermarkets = kwargs.get('max_supermarkets', None)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    user_cart_items = ProductEntry.objects.filter(cart=Cart.objects.get(user__username=user['username']), is_list_product=False)
    
    upgrading_dict = dict()
    
    for item in user_cart_items:
      
      if upgrading_dict.get(item.product_price.id, None) is None:
        upgrading_dict[item.product_price.id] = {
          'quantity': 0,
          'is_locked': 0,
        }
        upgrading_dict[item.product_price.id]['quantity'] = item.quantity
        upgrading_dict[item.product_price.id]['is_locked'] = item.locked
      else:
        upgrading_dict[item.product_price.id]['quantity'] = item.quantity
        upgrading_dict[item.product_price.id]['is_locked'] = item.locked
      
    if max_supermarkets and max_supermarkets < Supermarket.objects.all().count() and max_supermarkets > 0:
      improved_cart_prices = improve_cart(upgrading_dict, max_supermarkets)
      translate_cart_improvement_result(user_cart_items, improved_cart_prices)
    else:
      improved_cart_prices = improve_cart_optimization(upgrading_dict)
      translate_cart_optimization_improvement_result(user_cart_items, improved_cart_prices)
    
    return UpgradeCartMutation(entry=ProductEntry.objects.filter(cart=Cart.objects.get(user__username=user['username']), is_list_product=False))

class CreateListMutation(graphene.Mutation):
  class Input:
    user_token = graphene.String(required=True)
    list_name = graphene.String(required=True)
  
  list = graphene.Field(ListType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    user_token = kwargs.get('user_token', '')
    list_name = kwargs.get('list_name', '').strip()
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if not list_name:
      raise ValueError(_("The list name cannot be empty"))
    
    existing_entry = ProductEntry.objects.filter(cart__user__username=user['username'], is_list_product=False)
    
    if len(existing_entry) > 0:
      new_list = List.objects.create(user=KununuaUser.objects.get(username=user['username']), name=list_name)
      for entry in existing_entry:
        entry.list = new_list
        entry.is_list_product = True
        entry.cart = None
        entry.save()
      return CreateListMutation(list=new_list)
    else:
      raise ValueError(_("There are no products in the cart"))
    
class DeleteListMutation(graphene.Mutation):
  class Input:
    user_token = graphene.String(required=True)
    list_id = graphene.Int(required=True)
    
  is_deleted = graphene.Field(graphene.Boolean)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    user_token = kwargs.get('user_token', '')
    list_id = kwargs.get('list_id', None)
    
    try:
      user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
    except jwt.InvalidSignatureError:
      raise ValueError(_("Invalid token"))
    
    if list_id is None:
      raise ValueError(_("Invalid list"))
    
    try:
      selected_list = List.objects.get(pk=list_id)
    except List.DoesNotExist:
      raise ValueError(_("Invalid list"))
    
    if selected_list.user.username != user['username']:
      raise ValueError(_("Invalid list"))
    
    selected_list.delete()
    
    return DeleteListMutation(is_deleted=True)

class ProductsMutation(graphene.ObjectType):
  add_image_to_product = AddImageToProductMutation.Field()
  add_entry_to_cart = AddEntryToCartMutation.Field()
  edit_cart_entry = EditCartEntryMutation.Field()
  upgrade_cart = UpgradeCartMutation.Field()
  create_list = CreateListMutation.Field()
  delete_list = DeleteListMutation.Field()