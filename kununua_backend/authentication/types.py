import graphene
from graphene_django.types import DjangoObjectType
from authentication.models import KununuaUser
class KununuaUserType(DjangoObjectType):
  class Meta:
    model = KununuaUser