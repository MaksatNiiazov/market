from graphene_django.types import DjangoObjectType

from tanda_backend.merchant.models import Merchant


class MerchantType(DjangoObjectType):
    class Meta:
        model = Merchant
        fields = "__all__"
