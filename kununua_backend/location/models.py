from django.db import models
from django.utils.translation import gettext_lazy as _

class Currency(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    code = models.CharField(_("code"), max_length=3, unique=True)
    symbol = models.CharField(_("icon"), max_length=3, null=True)

    def __str__(self):
        return f"Currency[name: {self.name}, code: {self.code}, icon: {self.symbol}]"

class Country(models.Model):
    spanish_name = models.CharField(_("spanish_name"), max_length=64, unique=True)
    english_name = models.CharField(_("english_name"), max_length=64, unique=True)
    code = models.CharField(_("code"), max_length=3, unique=True)
    phone_code = models.CharField(_("phone_code"), max_length=6, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Country[name: {self.spanish_name}, code: {self.code}, currency: {self.currency.code}]"