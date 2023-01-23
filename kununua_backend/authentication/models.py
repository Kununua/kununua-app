from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from location.models import Country

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
        constraints = [
            models.UniqueConstraint(fields=["user", "value"], name='Unique user-value constraint'),
            models.UniqueConstraint(fields=["user", "name"], name='unique user-name constraint')
        ]
    
    def __str__(self):
        return f"Address[name: {self.name}, value: {self.value}, zipcode: {self.zipcode}, is_default: {self.is_default}, user: {self.user}]"