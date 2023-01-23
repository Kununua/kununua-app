import graphene
from graphene_django.types import DjangoObjectType
from authentication.models import KununuaUser
class KununuaUserType(DjangoObjectType):
  class Meta:
    model = KununuaUser
    
class AuthenticationQuery(object):
  
  get_user_by_username = graphene.Field(KununuaUserType, username=graphene.String())

  def resolve_get_user_by_username(self, info, username):
    return KununuaUser.objects.get(username=username)