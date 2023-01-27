import graphene
from .types import ProductType, CategoryType
from location.types import CountryType
from .models import Product, Category
from .utils.image_coder import encode_image


class ProductsQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())
  get_products_by_category = graphene.List(ProductType, category=graphene.String())

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
    product.image = encode_image(product.image.url)
  
    return product
  
  def resolve_get_products_by_category(self, info, category):
    
    products = Product.objects.filter(category__name=category)
    
    # Order products
    
    products = products[:50]
    
    for product in products:
        product.image = encode_image(product.image.url)
    
    return products
  
class CategoriesQuery(object):
  
  get_all_categories = graphene.List(CategoryType)
  
  def resolve_get_all_categories(self, info):
    return Category.objects.all().order_by('name')