import graphene
from graphene_django import DjangoObjectType
from graphql.type.definition import GraphQLResolveInfo

from .models import User
from ..merchant.graphql.types import MerchantType


class UserType(DjangoObjectType):
    merchant = graphene.Field(MerchantType)

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
            "sso_id",
        )

    def resolve_merchant(self, info: GraphQLResolveInfo, **kwargs):
        return self.merchant


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info: GraphQLResolveInfo, **kwargs):
        return info.context.user


schema = graphene.Schema(query=Query)
