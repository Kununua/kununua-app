import graphene
from .models import Country, Currency
from graphene_django.types import DjangoObjectType

class CountryType(DjangoObjectType):
  class Meta:
    model = Country
    
class CurrencyType(DjangoObjectType):
  class Meta:
    model = Currency