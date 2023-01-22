from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product

class PriceHistory(models.Model):
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    unit_price = models.CharField(_("unit_price"), max_length=16)
    date = models.DateTimeField(_("date"), auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def _str_(self):
        return f"PriceHistory[price: {self.price}, unit_price: {self.unit_price}, last_modified: {self.last_modified}, product: {self.product}]"

