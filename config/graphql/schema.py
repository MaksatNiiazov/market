import graphene

from tanda_backend.oauth import schema as oauth_schema
from tanda_backend.users import schema as users_schema
from tanda_backend.products.graphql.schema import schema as products_schema
from tanda_backend.merchant.graphql import mutations as merchant_mutations
from tanda_backend.merchant.graphql import schema as merchant_schema
from tanda_backend.products.graphql import mutations as products_mutations
from tanda_backend.orders.graphql import schema as orders_schema
from tanda_backend.orders.graphql import mutations as orders_mutations
from tanda_backend.payment.graphql import schema as payment_schema


class Query(
    users_schema.schema.Query,
    products_schema.Query,
    merchant_schema.Query,
    orders_schema.Query,
    payment_schema.Query,
    graphene.ObjectType,
):
    # Inherits all classes and methods from app-specific queries, so no need
    # to include additional code here.
    pass


class Mutation(
    merchant_mutations.Mutation,
    oauth_schema.schema.Mutation,
    products_mutations.Mutation,
    orders_mutations.Mutation,
    graphene.ObjectType,
):
    # Inherits all classes and methods from app-specific mutations, so no need
    # to include additional code here.
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
