import graphene
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from tanda_backend.orders.models import Order
from tanda_backend.payment.graphql.types import PaymentType
from tanda_backend.payment.models import Payment


class Query(graphene.ObjectType):
    payment = graphene.Field(PaymentType, order_id=graphene.ID(required=True))

    @login_required
    def resolve_payment(self, info, order_id: int):
        user = info.context.user
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise GraphQLError("Order not found")

        if order.user_id != user.id and (
            not getattr(user, "merchant", None) or order.merchant_id != getattr(user.merchant, "id", None)
        ):
            raise GraphQLError("Access denied")

        payment = Payment.objects.filter(order_id=order_id).first()
        if not payment:
            raise GraphQLError("Payment not found")
        return payment
