import graphene
from decimal import Decimal

from graphql.error.graphql_error import GraphQLError
from graphql_jwt.decorators import login_required

from tanda_backend.merchant.models import Merchant
from tanda_backend.products.graphql.types import ProductVariantInput, ProductType
from tanda_backend.products.services.create_product import create_product, CreatedProductVariant


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


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
