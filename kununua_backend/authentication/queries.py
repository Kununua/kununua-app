import graphene
from .types import KununuaUserType
from .models import KununuaUser

class AuthenticationQuery(object):
  
  get_user_by_username = graphene.Field(KununuaUserType, username=graphene.String())

  def resolve_get_user_by_username(self, info, username):
    return KununuaUser.objects.get(username=username)