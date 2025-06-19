import graphene
from decimal import Decimal

from graphql.error.graphql_error import GraphQLError
from graphql_jwt.decorators import login_required

from tanda_backend.merchant.models import Merchant
from tanda_backend.products.graphql.types import (
    ProductVariantInput,
    ProductType,
    ProductVariantType,
)
from tanda_backend.products.services.create_product import create_product, CreatedProductVariant
from tanda_backend.products.services.update_product import update_product
from tanda_backend.products.services.update_product_variant import update_product_variant
from tanda_backend.products.models import Product, ProductVariant


class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        merchant_id = graphene.Int(required=True)
        brand = graphene.String(required=True)
        product_variants = graphene.List(ProductVariantInput, required=True)

    product = graphene.Field(ProductType)

    @login_required
    def mutate(self, info, title, description, category_id, merchant_id, brand, product_variants):
        user = info.context.user
        merchant = Merchant.objects.filter(user=user, id=merchant_id).first()

        if not merchant:
            raise GraphQLError("Merchant not found.")

        variants = [
            CreatedProductVariant(
                article=variant.article,
                cost_price=Decimal(str(variant.cost_price)),
                selling_price=Decimal(str(variant.selling_price)),
                option_value_ids=variant.option_value_ids,
                image_id=variant.image_id
            ) for variant in product_variants
        ]

        product = create_product(
            title=title,
            description=description,
            category_id=category_id,
            merchant_id=merchant_id,
            brand=brand,
            product_variants=variants
        )
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        brand = graphene.String()

    product = graphene.Field(ProductType)

    @login_required
    def mutate(self, info, product_id, title=None, description=None, brand=None):
        user = info.context.user
        product = Product.objects.filter(id=product_id, merchant__user=user).first()

        if not product:
            raise GraphQLError("Product not found.")

        updated_product = update_product(
            product_id=product_id,
            title=title,
            description=description,
            brand=brand,
        )
        return UpdateProduct(product=updated_product)


class UpdateProductVariant(graphene.Mutation):
    class Arguments:
        variant_id = graphene.Int(required=True)
        article = graphene.String()
        cost_price = graphene.Decimal()
        selling_price = graphene.Decimal()
        option_value_ids = graphene.List(graphene.Int)
        image_id = graphene.Int()

    product_variant = graphene.Field(ProductVariantType)

    @login_required
    def mutate(
        self,
        info,
        variant_id,
        article=None,
        cost_price=None,
        selling_price=None,
        option_value_ids=None,
        image_id=None,
    ):
        user = info.context.user
        variant = ProductVariant.objects.filter(
            id=variant_id,
            product__merchant__user=user,
        ).first()

        if not variant:
            raise GraphQLError("Product variant not found.")

        updated_variant = update_product_variant(
            variant_id=variant_id,
            article=article,
            cost_price=Decimal(str(cost_price)) if cost_price is not None else None,
            selling_price=Decimal(str(selling_price)) if selling_price is not None else None,
            option_value_ids=option_value_ids,
            image_id=image_id,
        )

        return UpdateProductVariant(product_variant=updated_variant)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    update_product_variant = UpdateProductVariant.Field()
