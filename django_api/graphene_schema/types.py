import graphene
from graphene_django.types import DjangoObjectType
from django_api_app.models import User

class UserType(DjangoObjectType):
  class Meta:
    model = User
    
class Query(object):
  
  all_users = graphene.List(UserType)
  get_user_by_username = graphene.Field(UserType, username=graphene.String())
  log_user = graphene.Field(UserType, username=graphene.String(), password=graphene.String())

  def resolve_get_user_by_username(self, info, username):
    return User.objects.get(username=username)

  def resolve_all_users(self, info):
    return User.objects.all()

  def resolve_log_user(self, info, username, password):

    try:
      return User.objects.get(username=username, password=password)
    except:
      return None