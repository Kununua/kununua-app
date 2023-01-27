import graphene
from authentication.queries import AuthenticationQuery as SchemeAuthenticationQuery
from authentication.mutations import AuthenticationMutation as SchemeAuthenticationMutation
from products.queries import ProductsQuery as SchemeProductsQuery, CategoriesQuery as SchemeCategoriesQuery
from products.mutations import ProductsMutation as SchemeProductsMutation

class KununuaQuery(SchemeAuthenticationQuery, SchemeProductsQuery, SchemeCategoriesQuery, graphene.ObjectType):
  pass

class KununuaMutation(SchemeAuthenticationMutation, SchemeProductsMutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=KununuaQuery, mutation=KununuaMutation)