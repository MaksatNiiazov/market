from graphene_django.types import DjangoObjectType

from tanda_backend.payment.models import Payment


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = "__all__"

