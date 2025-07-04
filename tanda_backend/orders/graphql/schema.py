import graphene
from graphql_jwt.decorators import login_required

from tanda_backend.orders.graphql.types import OrderType
from tanda_backend.orders.models import Order


class Query(graphene.ObjectType):
    my_orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    @login_required
    def resolve_my_orders(self, info):
        user = info.context.user
        return Order.objects.filter(user=user)

    @login_required
    def resolve_order(self, info, id):
        user = info.context.user
        return Order.objects.get(user=user, id=id)
