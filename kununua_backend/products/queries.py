import graphene, base64
from .types import ProductType
from location.types import CountryType
from .models import Product


class ProductsQuery(object):
  
  get_product_by_id = graphene.Field(ProductType, id=graphene.Int())

  def resolve_get_product_by_id(self, info, id):
      
    product = Product.objects.get(pk=id)
    image_url = product.image.url
    
    if product.image.url.startswith("/"):
      image_url = image_url[1:]
    
    with open(image_url, "rb") as img:
      
        encoded_image = base64.b64encode(bytes(img.read()))
      
        product.image = encoded_image.decode("utf-8")
  
    return product