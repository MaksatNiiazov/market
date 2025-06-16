import graphene
from graphene_django.types import DjangoObjectType
from collections import defaultdict
from decimal import Decimal

from tanda_backend.products.models import Category, Product, ProductVariant, VariantOption, OptionValue, OptionType, Image, CategoryOptionRequirement


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children")


class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "product",
            "stock_id",
            "available_quantity",
            "created_at",
            "updated_at",
            "cost_price",
            "selling_price",
            "images",
            "variantoption_set",
        )


class OptionValueType(DjangoObjectType):
    class Meta:
        model = OptionValue
        fields = ("id", "option_type", "value", "meta_data")


class OptionTypeType(DjangoObjectType):
    class Meta:
        model = OptionType
        fields = ("id", "name", "code")


class CategoryOptionRequirementType(DjangoObjectType):
    class Meta:
        model = CategoryOptionRequirement
        fields = ("id", "category", "option_type", "is_main", "is_required", "sort_order")


class VariantOptionType(DjangoObjectType):
    class Meta:
        model = VariantOption
        fields = ("id", "product_variant", "option_value", "created_at", "updated_at")


class GroupedVariantType(graphene.ObjectType):
    option_value = graphene.Field(OptionValueType)
    variants = graphene.List(ProductVariantType)


class ProductType(DjangoObjectType):
    variants = graphene.List(ProductVariantType)
    grouped_variants = graphene.List(GroupedVariantType)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "images", "slug", "category",
                  "group_by_option_id", "stock_id", "provider_id", "created_at", "updated_at", "selling_price", "brand")

    def resolve_variants(self, info):
        return ProductVariant.objects.filter(product=self)

    def resolve_grouped_variants(self, info):
        variants = ProductVariant.objects.filter(product=self).prefetch_related('variantoption_set__option_value')

        if not self.group_by_option_id:
            return []

        group_option_type = self.group_by_option_id

        grouped_variants_dict = defaultdict(list)

        for variant in variants:
            option_value = None
            for variant_option in variant.variantoption_set.all():
                if variant_option.option_value and variant_option.option_value.option_type_id == group_option_type.id:
                    option_value = variant_option.option_value
                    break

            if option_value:
                grouped_variants_dict[option_value.id].append((option_value, variant))

        result = []
        for option_id, variants_data in grouped_variants_dict.items():
            if variants_data:
                option_value = variants_data[0][0]
                variants_list = [data[1] for data in variants_data]

                result.append(GroupedVariantType(
                    option_value=option_value,
                    variants=variants_list
                ))

        return result


class ProductPagination(graphene.ObjectType):
    total_count = graphene.Int()
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    items = graphene.List(ProductType)


class ProductVariantInput(graphene.InputObjectType):
    article = graphene.String(required=True)
    cost_price = graphene.Decimal(required=True)
    selling_price = graphene.Decimal(required=True)
    option_value_ids = graphene.List(graphene.Int, required=True)
    image_id = graphene.Int(required=True)
