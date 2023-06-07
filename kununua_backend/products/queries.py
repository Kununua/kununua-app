import graphene, jwt
from django.utils.translation import gettext_lazy as _
from .types import ProductType, CategoryType, ProductEntryType, ProductFilterType, FilterType, ListType, SupermarketType
from authentication.models import KununuaUser
from location.types import CountryType
from .models import Product, Category, Cart, ProductEntry, Rating, Price, List, Supermarket
from django.db.models import Q, Max


class ProductsQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())
  get_products_by_category = graphene.Field(ProductFilterType, category=graphene.String(), page_number=graphene.Int(required=False), limit=graphene.Int(required=False))
  get_products_by_supermarket = graphene.Field(ProductFilterType, supermarket_id=graphene.Int(), page_number=graphene.Int(required=False), limit=graphene.Int(required=False))
  get_products_with_offer = graphene.List(ProductType)
  get_packs = graphene.List(ProductType)

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
  
    return product
  
  def resolve_get_products_by_category(self, info, category, page_number=None, limit=None):
    
    if not page_number:
      page_number = 1
      
    if not limit:
      limit = 10
    
    min_pagination_index = limit * (page_number - 1)
    max_pagination_index = limit * page_number
    
    try:
      category = Category.objects.get(name=category)
    except Category.DoesNotExist:
      raise ValueError(_("Category does not exist"))
    
    products = Product.objects.filter(category=category).exclude(name__iexact='')[min_pagination_index:max_pagination_index]
    
    filters = _get_filters(products)
    
    return ProductFilterType(products=products, filters=filters)
  
  def resolve_get_products_by_supermarket(self, info, supermarket_id, page_number=None, limit=None):
    
    if not page_number:
      page_number = 1
      
    if not limit:
      limit = 10
    
    min_pagination_index = limit * (page_number - 1)
    max_pagination_index = limit * page_number
    
    try:
      supermarket = Supermarket.objects.get(pk=supermarket_id)
    except Category.DoesNotExist:
      raise ValueError(_("Category does not exist"))
    
    products = Product.objects.filter(price__supermarket=supermarket).exclude(name__iexact='')[min_pagination_index:max_pagination_index]
    
    filters = _get_filters(products)
    
    return ProductFilterType(products=products, filters=filters)

  def resolve_get_products_with_offer(self, info):
    
    products = Product.objects.filter(price__amount=1).exclude(image="products/images/nodisponible.png").distinct()[:20]
    
    return products
  
  def resolve_get_packs(self, info):
    
    products = Product.objects.filter(price__amount__gt=1).distinct()[:20]
    
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

class ListsQuery(object):
    
    get_lists = graphene.List(ListType, user_token=graphene.String())
    
    def resolve_get_lists(self, info, user_token):
      
      try:
        user = jwt.decode(user_token, 'my_secret', algorithms=['HS256'])
      except jwt.InvalidSignatureError:
        raise ValueError(_("Invalid token"))
      
      try:
        user = KununuaUser.objects.get(username=user['username'])
      except KununuaUser.DoesNotExist:
        raise ValueError(_("User does not exist"))
      
      return List.objects.filter(user=user)
  
class FilterQuery(object):
  
  filter_products = graphene.List(ProductType, supermarkets=graphene.List(graphene.String, required=False), categories=graphene.List(graphene.String, required=False), brands=graphene.List(graphene.String, required=False), min_rating=graphene.Float(required=False), max_rating=graphene.Float(required=False), min_price=graphene.Float(required=False), max_price=graphene.Float(required=False), name=graphene.String(required=False), page_number=graphene.Int(required=False), limit=graphene.Int(required=False))
  get_products_by_name = graphene.Field(ProductFilterType, name=graphene.String(), page_number=graphene.Int(required=False), limit=graphene.Int(required=False))
  
  def resolve_filter_products(self, info, supermarkets=None, categories=None, brands=None, min_rating=None, max_rating=None, min_price=None, max_price=None, name=None, page_number=None, limit=None):
    
    if not page_number:
      page_number = 1
      
    if not limit:
      limit = 10
    
    min_pagination_index = limit * (page_number - 1)
    max_pagination_index = limit * page_number
    
    q = Q()

    if name and name.strip() != '':
      q &= Q(name__icontains=name.strip())
      q |= Q(brand__name__icontains=name.strip())
      q |= Q(category__name__icontains=name.strip())

    if supermarkets:
      supermarkets = set(supermarkets)
      q &= Q(price__supermarket__name__in=supermarkets)
      
    if brands:
      brands = set(brands)
      q &= Q(brand__name__in=brands)
    
    if min_price:
      q &= Q(price__price__gte=min_price)
    
    if max_price:
      q &= Q(price__price__lte=max_price)
    
    products = Product.objects.filter(q).distinct()

    if categories or min_rating or max_rating:
      result = []
      if categories:
        categories = set(categories)
        categories = [category.lower().strip() for category in categories]
      for product in products:
        if len(result) == limit:
          break
        if categories:
          category = product.category
          if not _has_category(category, categories):
            continue
        if min_rating or max_rating:
          avg = product.get_average_rating()
          avg = avg if avg else 0
          if not (min_rating and max_rating and min_rating <= avg <= max_rating) and not (min_rating and min_rating <= avg) and not (max_rating and max_rating >= avg):
            continue
        result.append(product)
  
      return result
    
    return products[min_pagination_index:max_pagination_index]  
  
  def resolve_get_products_by_name(self, info, name, page_number=None, limit=None):
    
    if not page_number:
      page_number = 1
      
    if not limit:
      limit = 10
    
    min_pagination_index = limit * (page_number - 1)
    max_pagination_index = limit * page_number
    
    q = Q()
    if name and name.strip() != '':
      q &= Q(name__icontains=name.strip())
      q |= Q(brand__name__icontains=name.strip())
      q |= Q(category__name__icontains=name.strip())
      products = Product.objects.filter(q).distinct()
    else:
      raise ValueError(_("Name is required"))
    
    products = products[min_pagination_index:max_pagination_index]
    filters = _get_filters(products)
    
    return ProductFilterType(products = products, filters = filters)
          
  
def _has_category(category, categories):
  if str(category.name).lower().strip() in categories:
    return True
  
  if category.parent != None:
    return _has_category(category.parent, categories)
    
  return False

def _get_filters(products):
  supermarkets = []
  brands = []
  categories = []
  min_price = 0
  max_price = 0
  min_rating = 0
  max_rating = 0
  
  
  for product in products:
    if product.brand and product.brand.name not in brands:
      brands.append(product.brand.name)
    if product.category.name not in categories:
      categories.append(product.category.name)
    for price in Price.objects.filter(product=product):
      if price.supermarket.name not in supermarkets:
        supermarkets.append(price.supermarket.name)
      if price.price < min_price or min_price == 0:
        min_price = price.price
      if price.price > max_price:
        max_price = price.price
    if not (min_rating == 0 and max_rating == Rating.objects.all().aggregate(Max('rating'))['rating__max']):
      avg = product.get_average_rating()
      avg = avg if avg else 0
      if avg < min_rating or min_rating == 0:
        min_rating = avg
      if avg > max_rating:
        max_rating = avg
  
  filter1 = FilterType(key='Supermercados', options=supermarkets)
  filter2 = FilterType(key='Marcas', options=brands)
  filter3 = FilterType(key='Categorías', options=categories)
  filter4 = FilterType(key='Precio', options=[round(min_price), round(max_price), round(min_price), round(max_price)])
  filter5 = FilterType(key='Puntuación', options=[round(min_rating), round(max_rating), round(min_rating), round(max_rating)])
  
  return [filter1, filter2, filter3, filter4, filter5]

class SupermarketsQuery(object):
  
  get_supermarkets = graphene.List(SupermarketType)
  
  def resolve_get_supermarkets(self, info):
    return Supermarket.objects.all()