import graphene
import graphql_jwt
from django_api_app.models import KununuaUser
from .types import *
from django.contrib.auth import authenticate

class LogUserMutation(graphene.Mutation):
  
  class Input:
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    
  user = graphene.Field(KununuaUserType)
  
  @staticmethod
  def mutate(root, info, **kwargs):
    username = kwargs.get('username', '').strip()
    password = kwargs.get('password', '').strip()
    
    user = authenticate(username=username, password=password)
    
    if user == None:
      return None
    
    return LogUserMutation(user=user)

class CreateUserMutation(graphene.Mutation):

  class Input:
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String(required=True)
    surname = graphene.String(required=True)
    email = graphene.String(required=True)

  user = graphene.Field(KununuaUserType)

  @staticmethod
  def mutate(root, info, **kwargs):
    username = kwargs.get('username', '').strip()
    password = kwargs.get("password", '').strip()
    first_name = kwargs.get("name", "").strip()
    last_name = kwargs.get("surname", "").strip()
    email = kwargs.get("email", "").strip()
    
    if len(username) < 6 or username > 25 or username == "" or username == None:
      return None
    
    if len(password) < 6 or password == "" or password == None:
      return None
    
    if len(first_name) < 3 or first_name >= 50 or first_name == "" or first_name == None:
      return None
    
    if len(last_name) < 3 or last_name >= 50 or last_name == "" or last_name == None:
      return None
    
    if email == "" or email == None or (not "@" in email) or (not "." in email):
      return None
    
    obj = KununuaUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=None, profile_picture="/assets/user-images/default.png")
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

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(KununuaUserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class Mutation(graphene.ObjectType):
  token_auth = ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  log_user = LogUserMutation.Field()
  create_user = CreateUserMutation.Field()
  delete_user = DeleteUserMutation.Field()