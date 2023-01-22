import graphene
from authentication.types import AuthenticationQuery as SchemeAuthenticationQuery
from authentication.mutation import Mutation as SchemeMutation

class KununuaQuery(SchemeAuthenticationQuery, graphene.ObjectType):
  pass

class KununuaMutation(SchemeMutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=KununuaQuery, mutation=KununuaMutation)