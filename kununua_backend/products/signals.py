from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver
from products.models import ProductEntry
from django.conf import settings
from whoosh import index
from scripts.bazar_api_index import PRODUCT_SCHEMA
import os

@receiver(pre_save, sender=ProductEntry)
def make_field_null(sender, instance, **kwargs):
    if instance.is_list_product:
        instance.cart = None
    else:
        instance.list = None

    if not instance.cart and not instance.list:
        raise ValidationError(_("The product must be either in a cart or a list."))
    
@receiver(post_migrate, sender=None)
def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.makedirs(settings.WHOOSH_INDEX, exist_ok=True)
        index.create_in(settings.WHOOSH_INDEX, schema=PRODUCT_SCHEMA)
   