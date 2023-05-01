from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import KununuaUser
from location.models import Country

class Supermarket(models.Model):
    name = models.CharField(_("name"), max_length=64)
    zipcode = models.CharField(_("zipcode"), max_length=10)
    main_url = models.URLField(_("main_url"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'country', 'zipcode'], name='unique_supermarket')
        ]
    
    def __str__(self):
        return f"Supermarket[name: {self.name}, zipcode: {self.zipcode}, main_url: {self.main_url}, country: {self.country}]"
        
class Category(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Category[name: {self.name}, parent: {self.parent.name if self.parent else None}]"

class Brand(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True, default=_("Marca blanca"))
    
    def __str__(self):
        return f"Brand[name: {self.name}]"

class Product(models.Model):
    name = models.CharField(_("name"), max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, null=True)
    image = models.ImageField(_("image"), upload_to="products/images/", null=True, max_length=1024)
    is_vegetarian = models.BooleanField(_("is_vegetarian"), default=False, null=True)
    is_gluten_free = models.BooleanField(_("is_gluten_free"), default=False, null=True)
    is_freezed = models.BooleanField(_("is_freezed"), default=False, null=True)
    is_from_country = models.BooleanField(_("is_from_country"), default=False, null=True)
    is_eco = models.BooleanField(_("is_eco"), default=False, null=True)
    is_without_sugar = models.BooleanField(_("is_without_sugar"), default=False, null=True)
    is_without_lactose = models.BooleanField(_("is_without_lactose"), default=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    def get_average_rating(self):
        return Rating.objects.filter(product=self).aggregate(models.Avg('rating'))['rating__avg']
    
    def __str__(self):
        return f"Product[name: {self.name}, brand: {self.brand}]"

class Price(models.Model):
    
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    weight = models.CharField(_("weight"), max_length=24, null=True)
    amount = models.PositiveIntegerField(_("amount"), null=True)
    url = models.URLField(_("url"), null=True, max_length=1024)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"Product[name: {self.product.name}, price: {self.price}, amount: {self.amount}, supermarket: {self.supermarket.name}, url: {self.url}]"
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_rating')
        ]
        
    def _str_(self):
        return f"Rating[product: {self.product}, user: {self.user}, rating: {self.rating}]"
    
class List(models.Model):
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    
    def __str__(self):
        return f"List[date: {self.date}, user: {self.user}]"

class Cart(models.Model):
    user = models.OneToOneField(KununuaUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart[user: {self.user}]"

class ProductEntry(models.Model):
    quantity = models.PositiveIntegerField(_("quantity"))
    locked = models.BooleanField(_("locked"), default=False)
    product_price = models.ForeignKey(Price, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_list_product = models.BooleanField(_("is_list_product"), default=False)
    
    def __str__(self):
        return f"ProductEntry[quantity: {self.quantity}, product: {self.product_price}, list: {self.list}, cart: {self.cart}, is_list_product: {self.is_list_product}]"
