import graphene
from graphene_django.types import DjangoObjectType
from django_api_app.models import User

class UserType(DjangoObjectType):
  class Meta:
    model = User
    
class Query(object):
  
  all_users = graphene.List(UserType)

  def resolve_all_users(self, info):
    return User.objects.all()