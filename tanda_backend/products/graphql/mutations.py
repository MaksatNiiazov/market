from decimal import Decimal

import graphene
from graphql.error.graphql_error import GraphQLError
from graphql_jwt.decorators import login_required

from tanda_backend.merchant.models import Merchant
from tanda_backend.products.graphql.types import ProductType
from tanda_backend.products.graphql.types import ProductVariantInput
from tanda_backend.products.models import Product
from tanda_backend.products.services import update_product
from tanda_backend.products.services.create_product import CreatedProductVariant
from tanda_backend.products.services.create_product import create_product


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
    def mutate(self, info, title, description, category_id, merchant_id, brand, product_variants):  # noqa: PLR0913
        user = info.context.user
        merchant = Merchant.objects.filter(user=user, id=merchant_id).first()

        if not merchant:
            message = "Merchant not found."
            raise GraphQLError(message)

        variants = [
            CreatedProductVariant(
                article=variant.article,
                cost_price=Decimal(str(variant.cost_price)),
                selling_price=Decimal(str(variant.selling_price)),
                option_value_ids=variant.option_value_ids,
                image_id=variant.image_id,
            ) for variant in product_variants
        ]

        product = create_product(
            title=title,
            description=description,
            category_id=category_id,
            merchant_id=merchant_id,
            brand=brand,
            product_variants=variants,
        )
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        category_id = graphene.Int()
        brand = graphene.String()

    product = graphene.Field(ProductType)

    @login_required
    def mutate(self, info, product_id, title=None, description=None, category_id=None, brand=None):  # noqa: PLR0913
        user = info.context.user
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as err:
            message = "Product not found."
            raise GraphQLError(message) from err

        if not Merchant.objects.filter(user=user, id=product.merchant_id).exists():
            message = "Merchant not found."
            raise GraphQLError(message)

        updated_product = update_product(
            product_id=product_id,
            title=title,
            description=description,
            category_id=category_id,
            brand=brand,
        )
        return UpdateProduct(product=updated_product)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
