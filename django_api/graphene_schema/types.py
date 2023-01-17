import graphene
from graphene_django.types import DjangoObjectType
from django_api_app.models import KununuaUser

class KununuaUserType(DjangoObjectType):
  class Meta:
    model = KununuaUser
    
class Query(object):
  
  all_users = graphene.List(KununuaUserType)
  get_user_by_username = graphene.Field(KununuaUserType, username=graphene.String())
  log_user = graphene.Field(KununuaUserType, username=graphene.String(), password=graphene.String())

  def resolve_get_user_by_username(self, info, username):
    return KununuaUser.objects.get(username=username)

  def resolve_all_users(self, info):
    return KununuaUser.objects.all()

  def resolve_log_user(self, info, username, password):

    try:
      return KununuaUser.objects.get(username=username, password=password)
    except:
      return None