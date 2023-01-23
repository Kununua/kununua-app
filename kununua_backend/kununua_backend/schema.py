import graphene
from authentication.types import AuthenticationQuery as SchemeAuthenticationQuery
from authentication.mutation import Mutation as SchemeAuthenticationMutation
from products.types import ProductQuery as SchemeProductQuery
from products.mutations import Mutation as SchemeProductMutation

class KununuaQuery(SchemeAuthenticationQuery, SchemeProductQuery, graphene.ObjectType):
  pass

class KununuaMutation(SchemeAuthenticationMutation, SchemeProductMutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=KununuaQuery, mutation=KununuaMutation)