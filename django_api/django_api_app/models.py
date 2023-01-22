from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Currency(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    icon = models.CharField(_("icon"), max_length=3, unique=True)

    def __str__(self):
        return f"Currency[name: {self.name}, icon: {self.icon}]"

class Country(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Country[name: {self.name}, currency: {self.currency}]"
    
class KununuaUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone_number"), max_length=20, null=True)
    profile_picture = models.ImageField(_("profile_picture"), upload_to='profile_pictures', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"User[username: {self.username}, first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}]"
    
class Address(models.Model):
    name = models.CharField(_("name"), max_length=64)
    value = models.CharField(_("value"), max_length=256)
    zipcode = models.CharField(_("zipcode"), max_length=10)
    is_default = models.BooleanField(_("is_default"), default=False)
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'value'), ('user', 'name')
        constraints = [
            models.UniqueConstraint(fields=('user',), condition=Q(is_default=True), name=_('one_default_per_user'))
        ]
    
    def __str__(self):
        return f"Address[name: {self.name}, value: {self.value}, zipcode: {self.zipcode}, is_default: {self.is_default}, user: {self.user}]"
    
class Supermarket(models.Model):
    name = models.CharField(_("name"), max_length=64)
    zipcode = models.CharField(_("zipcode"), max_length=10)
    main_url = models.URLField(_("main_url"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'country', 'zipcode')
    
    def __str__(self):
        return f"Supermarket[name: {self.name}, zipcode: {self.zipcode}, main_url: {self.main_url}, country: {self.country}]"
        
class Category(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    
    def __str__(self):
        return f"Category[name: {self.name}]"

class Product(models.Model):
    name = models.CharField(_("name"), max_length=256)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    unit_price = models.CharField(_("unit_price"), max_length=16)
    url = models.URLField(_("url"), unique=True)
    is_vegetarian = models.BooleanField(_("is_vegetarian"), default=False, null=True)
    is_gluten_free = models.BooleanField(_("is_gluten_free"), default=False, null=True)
    is_freezed = models.BooleanField(_("is_freezed"), default=False, null=True)
    is_from_country = models.BooleanField(_("is_from_country"), default=False, null=True)
    offer_price = models.DecimalField(_("offer_price"), max_digits=10, decimal_places=2, null=True)
    unit_offer_price = models.CharField(_("unit_offer_price"), max_length=16, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    
    @property
    def weight_unit(self):
        return get_weight_unit(self)
    
    def get_average_rating(self):
        return Rating.objects.filter(product=self).aggregate(models.Avg('rating'))['rating__avg']
    
    def __str__(self):
        return f"Product[name: {self.name}, price: {self.price}, unit_price: {self.unit_price}, url: {self.url}]"
    
class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('product', 'user')
        
    def _str_(self):
        return f"Rating[product: {self.product}, user: {self.user}, rating: {self.rating}]"
    
    
class PriceHistory(models.Model):
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    unit_price = models.CharField(_("unit_price"), max_length=16)
    last_modified = models.DateTimeField(_("last_modified"), auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    @property
    def weight_unit(self):
        return get_weight_unit(self)
    
    def _str_(self):
        return f"PriceHistory[price: {self.price}, unit_price: {self.unit_price}, last_modified: {self.last_modified}, product: {self.product}]"

class List(models.Model):
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    
    def __str__(self):
        return f"List[date: {self.date}, user: {self.user}]"

class Cart(models.Model):
    user = models.ForeignKey(KununuaUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart[user: {self.user}]"

class ProductEntry(models.Model):
    quantity = models.PositiveIntegerField(_("quantity"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_list_product = models.BooleanField(_("is_list_product"), default=False)
    
    def __str__(self):
        return f"ProductEntry[quantity: {self.quantity}, product: {self.product}, list: {self.list}, cart: {self.cart}, is_list_product: {self.is_list_product}]"

# Auxiliary functions
def get_weight_unit(object):
    return "NotImplemented"

# Signals
@receiver(pre_save, sender=ProductEntry)
def make_field_null(sender, instance, **kwargs):
    if instance.is_list_product:
        instance.cart = None
    else:
        instance.list = None

    if not instance.cart and not instance.list:
        raise ValidationError(_("The product must be either in a cart or a list."))

pre_save.connect(make_field_null, sender=ProductEntry)