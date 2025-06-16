from graphene_django.types import DjangoObjectType

from tanda_backend.orders.models import Order, OrderItem


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"
