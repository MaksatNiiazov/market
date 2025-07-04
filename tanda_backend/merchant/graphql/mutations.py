import graphene
from esdbclient import NewEvent
from graphql_jwt.decorators import login_required
from django.db import transaction
from graphql import GraphQLError

from tanda_backend.common.eventstore import serialize, append_to_stream
from tanda_backend.merchant.graphql.types import MerchantType
from tanda_backend.merchant.models import Merchant
from tanda_backend.merchant.services.order_process import process_order
from tanda_backend.orders.models import Order, OrderStatus
from tanda_backend.orders.services.order_events import send_order_status_changed_event


class CreateMerchantMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        phone_number = graphene.String()
        address = graphene.String()
        document = graphene.String()
        account_number = graphene.String()
        birthday = graphene.types.datetime.Date()
        telegram = graphene.String()
        address_of_residence = graphene.String()
        inn = graphene.String()
        id_passport = graphene.String()
        additional_info = graphene.String()
        fio = graphene.String()

    merchant = graphene.Field(MerchantType)

    @login_required
    @transaction.atomic
    def mutate(self, info, name, **kwargs):
        user = info.context.user
        if Merchant.objects.filter(user=user).exists():
            raise GraphQLError("User already has a merchant")

        merchant = Merchant(user=user, name=name)

        for field in [
            'phone_number', 'address', 'document', 'account_number', 'birthday',
            'telegram', 'address_of_residence', 'inn', 'id_passport', 'additional_info']:
            if field in kwargs and kwargs[field] is not None:
                setattr(merchant, field, kwargs[field])

        if kwargs.get("fio"):
            user.fio = kwargs.get("fio")
            user.save()

        merchant.save()
        event = NewEvent(
            type="MerchantCreated",
            data=serialize(merchant.get_json()),
        )
        append_to_stream(event, "merchants")
        return CreateMerchantMutation(merchant=merchant)


class ProcessOrderStatus(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    @transaction.atomic
    def mutate(self, info, order_id, **kwargs):
        try:
            order = Order.objects.select_for_update().get(id=order_id)
        except Order.DoesNotExist:
            return ProcessOrderStatus(success=False, message="Order not found")

        if order.merchant.id != info.context.user.merchant.id:
            raise GraphQLError("Access denied, merchant not found")

        try:
            process_order(order)
            return ProcessOrderStatus(
                success=True,
                message=f"Successfully changed status."
            )
        except ValueError as e:
            return ProcessOrderStatus(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    create_merchant = CreateMerchantMutation.Field()
    process_order_status = ProcessOrderStatus.Field()
