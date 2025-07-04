import graphene
from django.db.models import Q
from decimal import Decimal

from tanda_backend.products.graphql.types import (
    CategoryType, ProductType, ProductPagination, CategoryOptionRequirementType, OptionValueType
)
from tanda_backend.products.models import Category, Product, OptionValue
from tanda_backend.products.services.category_option_requirements import get_option_requirements_by_category


class Query(graphene.ObjectType):
    categories_tree = graphene.List(CategoryType)
    products = graphene.Field(
        ProductPagination,
        search=graphene.String(),
        category_id=graphene.ID(),
        provider_id=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
        merchant_id=graphene.ID(),
    )
    product = graphene.Field(ProductType, id=graphene.ID())
    category_options = graphene.List(CategoryOptionRequirementType, category_id=graphene.ID(required=True))
    option_values = graphene.List(
        OptionValueType,
        option_type_id=graphene.ID(required=True),
        search=graphene.String(required=False),
        limit=graphene.Int(required=False),
        offset=graphene.Int(required=False),
    )

    def resolve_product(self, info, id: int):
        return Product.objects.get(id=id, is_approved=True)

    def resolve_categories_tree(self, info):
        return Category.objects.filter(parent=None).prefetch_related('children')

    def resolve_category_options(self, info, category_id: int):
        return get_option_requirements_by_category(category_id=category_id)

    def resolve_option_values(self, info, option_type_id: int, search: str = None, limit: int = 10, offset: int = 0):
        query = OptionValue.objects.filter(option_type_id=option_type_id)

        if search:
            query = query.filter(value__icontains=search)

        query = query.order_by('id')

        if offset > 0:
            query = query[offset:]
        results = query[:limit]
        return results

    def resolve_products(
        self,
        info,
        search=None,
        category_id=None,
        provider_id=None,
        merchant_id=None,
        limit=10,
        offset=0,
    ):
        query = Product.objects.filter(
            is_approved=True,
            productvariant__isnull=False
        ).order_by('id').distinct()

        filters = Q()
        if search:
            filters &= Q(title__icontains=search) | Q(description__icontains=search)

        if category_id:
            filters &= Q(category_id=category_id)

        if provider_id:
            filters &= Q(provider_id=provider_id)

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


schema = graphene.Schema(query=Query)
