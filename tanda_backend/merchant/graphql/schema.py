import graphene

from django.db.models import Q
from django.db import models
from graphene_django.types import DjangoObjectType
from graphql.error.graphql_error import GraphQLError

from graphql_jwt.decorators import login_required

from tanda_backend.orders.models import Order
from tanda_backend.products.graphql.types import ProductPagination
from tanda_backend.products.models import Product


class KanbanCardOrderType(DjangoObjectType):
    item_amount = graphene.Int()
    price_sum = graphene.Decimal()

    class Meta:
        model = Order
        fields = "__all__"


class Query(graphene.ObjectType):
    my_products = graphene.Field(
        ProductPagination,
        search=graphene.String(),
        category_id=graphene.ID(),
        limit=graphene.Int(),
        offset=graphene.Int(),
        merchant_id=graphene.ID(required=True),
    )
    kanban_cards = graphene.List(
        KanbanCardOrderType,
        merchant_id=graphene.ID(required=True),
    )
    detail_kandan_card = graphene.Field(
        KanbanCardOrderType,
        order_id=graphene.ID(required=True),
    )

    @login_required
    def resolve_detail_kandan_card(self, info, order_id: int):
        if not info.context.user.merchant:
            return []

        order = Order.objects.annotate(
            item_amount=models.Count("order_items"),
            price_sum=models.Sum("order_items__selling_price"),
        ).get(
            merchant=info.context.user.merchant,
            id=order_id
        )

        if order.merchant.id != info.context.user.merchant.id:
            raise GraphQLError("Access denied, merchant not found")

        return order

    @login_required
    def resolve_kanban_cards(self, info, merchant_id: int):
        if not info.context.user.merchant:
            return []

        if int(merchant_id) != info.context.user.merchant.id:
            raise GraphQLError("Access denied, merchant not found")

        return Order.objects.filter(
            merchant=info.context.user.merchant,
        ).annotate(
            item_amount=models.Count("order_items"),
            price_sum=models.Sum("order_items__selling_price"),
        ).order_by("created_at")

    @login_required
    def resolve_my_products(
        self,
        info,
        merchant_id: int,
        search=None,
        category_id=None,
        limit=10,
        offset=0,
    ):
        if not info.context.user.merchant:
            return ProductPagination(
                total_count=0,
                has_next_page=False,
                has_previous_page=False,
                items=[],
            )

        if int(merchant_id) != info.context.user.merchant.id:
            raise GraphQLError("Access denied, merchant not found")

        query = Product.objects.filter(
            merchant=info.context.user.merchant,
        ).order_by('id')

        filters = Q()
        if search:
            filters &= Q(title__icontains=search) | Q(description__icontains=search)

        if category_id:
            filters &= Q(category_id=category_id)

        if merchant_id:
            filters &= Q(merchant_id=merchant_id)

        if filters:
            query = query.filter(filters)

        total_count = query.count()

        if offset > 0:
            query = query[offset:]

        products = query[:limit]

        has_next_page = total_count > (offset + limit)
        has_previous_page = offset > 0

        return ProductPagination(
            total_count=total_count,
            has_next_page=has_next_page,
            has_previous_page=has_previous_page,
            items=products
        )
