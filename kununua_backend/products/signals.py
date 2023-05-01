from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from products.models import ProductEntry

@receiver(pre_save, sender=ProductEntry)
def make_field_null(sender, instance, **kwargs):
    if instance.is_list_product:
        instance.cart = None
    else:
        instance.list = None

    if not instance.cart and not instance.list:
        raise ValidationError(_("The product must be either in a cart or a list."))
   