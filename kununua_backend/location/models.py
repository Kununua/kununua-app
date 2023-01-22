from django.db import models
from django.utils.translation import gettext_lazy as _

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