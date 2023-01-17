import graphene
from django_api_app.models import KununuaUser
from .types import *

class CreateUserMutation(graphene.Mutation):

  class Input:
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String()
    surname = graphene.String()
    direction = graphene.String()
    email = graphene.String()
    phone_number = graphene.String()

  user = graphene.Field(KununuaUserType)

  @staticmethod
  def mutate(root, info, **kwargs):
    username = kwargs.get('username', '').strip()
    password = kwargs.get("password", '').strip()
    first_name = kwargs.get("name", "").strip()
    last_name = kwargs.get("surname", "").strip()
    email = kwargs.get("email", "").strip()
    phone_number = kwargs.get("phone_number", "").strip()
    obj = KununuaUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    return CreateUserMutation(user=obj)

class DeleteUserMutation(graphene.Mutation):

  class Input:
    username = graphene.String(required=True)

  user = graphene.Field(KununuaUserType)

  @staticmethod
  def mutate(root, info, **kwargs):
    username = kwargs.get('username', '').strip()
    
    selected_user = KununuaUser.objects.get(username=username)

    selected_user.delete()
    
    return DeleteUserMutation(user=selected_user)


class Mutation(graphene.ObjectType):
  create_user = CreateUserMutation.Field()
  delete_user = DeleteUserMutation.Field()