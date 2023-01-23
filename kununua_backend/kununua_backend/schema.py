import graphene
from authentication.types import AuthenticationQuery as SchemeAuthenticationQuery
from authentication.mutation import Mutation as SchemeAuthenticationMutation
from products.types import ProductsQuery as SchemeProductsQuery
from products.mutations import Mutation as SchemeProductMutation

class KununuaQuery(SchemeAuthenticationQuery, SchemeProductsQuery, graphene.ObjectType):
  pass

class KununuaMutation(SchemeAuthenticationMutation, SchemeProductMutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=KununuaQuery, mutation=KununuaMutation)