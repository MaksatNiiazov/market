import graphene
from graphql_jwt.decorators import login_required
from django.db import transaction

from tanda_backend.orders.graphql.types import OrderType
from tanda_backend.orders.models import PaymentType, DeliveryType
from tanda_backend.orders.services import create_orders


class VariantInput(graphene.InputObjectType):
    variant_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)


class CreateOrder(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        address = graphene.String(required=True)
        city = graphene.String(required=True)
        delivery_method = graphene.String(required=True)
        payment_method = graphene.String(required=True)
        comments = graphene.String()
        variants = graphene.List(VariantInput, required=True)

    orders = graphene.List(OrderType)

    @login_required
    @transaction.atomic
    def mutate(
        self, info,
        full_name,
        phone_number,
        address,
        city,
        delivery_method,
        payment_method,
        variants,
        comments: str = None,
    ):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("User is not authenticated")
        try:
            PaymentType(payment_method)
        except ValueError:
            raise Exception("Invalid payment method")

        try:
            DeliveryType(delivery_method)
        except ValueError:
            raise Exception("Invalid delivery method")

        orders = create_orders(
            user=user,
            full_name=full_name,
            phone_number=phone_number,
            payment_type=payment_method,
            city=city,
            address=address,
            delivery_type=delivery_method,
            comments=comments,
            variants=variants
        )
        return CreateOrder(orders=orders)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
