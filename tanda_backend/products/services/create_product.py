import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from urllib.parse import urlparse

from django.db import transaction
from django.utils.text import slugify

from tanda_backend.merchant.models import Merchant
from tanda_backend.products.models import OptionValue, Product, ProductVariant, VariantOption, Image, Category, OptionType
from tanda_backend.products.services.category_option_requirements import get_option_requirements_by_category, \
    get_main_option_by_category
from tanda_backend.products.services.external_product_service import create_external_product, \
    ExternalProductCreateRequest, \
    ExternalProductCreateSchema, ExternalProductVariantCreateSchema, Sex, SourceService


@dataclass
class CreatedProductVariant:
    article: str
    cost_price: Decimal
    selling_price: Decimal
    option_value_ids: list[int]
    image_id: int


def create_product(
    title: str,
    description: str,
    category_id: int,
    merchant_id: int,
    brand: str,
    product_variants: list[CreatedProductVariant],
    sex: Optional[Sex] = None
):
    merchant = Merchant.objects.get(id=merchant_id)

    if not merchant.is_approved or merchant.provider is None:
        raise ValueError("Merchant is not verified, please contact support.")

    required_options = get_option_requirements_by_category(category_id=category_id)
    main_option = get_main_option_by_category(category_id=category_id)

    if not product_variants:
        raise ValueError("Variants is required.")

    if not main_option:
        raise ValueError("Main option is required.")

    all_option_value_ids = []
    for variant in product_variants:
        all_option_value_ids.extend(variant.option_value_ids)

    option_values = OptionValue.objects.filter(id__in=all_option_value_ids).select_related('option_type')
    option_value_dict = {ov.id: ov for ov in option_values}

    for number, variant in enumerate(product_variants):
        for value_id in variant.option_value_ids:
            if value_id not in option_value_dict:
                raise ValueError(f"Value option with ID {value_id} does not exist.")

        variant_option_types = set()
        for value_id in variant.option_value_ids:
            variant_option_types.add(option_value_dict[value_id].option_type_id)

        for req in required_options:
            if req.is_required and req.option_type_id not in variant_option_types:
                raise ValueError(f"For variant {number + 1} required option not specified '{req.option_type.name}'")

    with transaction.atomic():
        articles = [variant.article for variant in product_variants]
        duplicate_articles = set([article for article in articles if articles.count(article) > 1])
        if duplicate_articles:
            raise ValueError(f"Duplicate article(s) found in request: {', '.join(duplicate_articles)}")

        existing_articles = ProductVariant.objects.filter(
            article__in=articles,
            product__merchant_id=merchant_id
        ).values_list('article', flat=True)

        if existing_articles:
            raise ValueError(f"Article(s) already exist for this merchant: {', '.join(existing_articles)}")

        images = {variant.image_id: Image.objects.get(id=variant.image_id) for
                  variant in product_variants}

        category = Category.objects.get(id=category_id)

        external_product_info = ExternalProductCreateSchema(
            title=title,
            supplier=merchant.name,
            category_public_id=str(category.public_id),
            brand=brand,
            sex=sex,
            description=description,
            photo_path=urlparse(list(images.values())[0].file.url).path.lstrip("/") if images else "",
            provider_id=str(merchant.provider.public_id)
        )

        external_variants = []
        for variant_data in product_variants:
            option_values = OptionValue.objects.filter(id__in=variant_data.option_value_ids).select_related('option_type')

            external_variants.append(ExternalProductVariantCreateSchema(
                sku=variant_data.article,
                base_price=float(variant_data.selling_price),
                cost_price=float(variant_data.cost_price),
                options_public_ids=[str(ov.public_id) for ov in option_values],
                photo_path=urlparse(images.get(variant_data.image_id).file.url).path.lstrip("/") if variant_data.image_id in images else ""
            ))

        external_request = ExternalProductCreateRequest(
            information=external_product_info,
            variants=external_variants,
            source_service=SourceService.TANDA,
        )

        external_response = create_external_product(external_request)

        product = Product.objects.create(
            title=title,
            description=description,
            brand=brand,
            images=[urlparse(image.file.url).path.lstrip("/") for image in images.values()],
            slug=slugify(title),
            category_id=category_id,
            group_by_option_id=main_option.option_type,
            merchant=merchant,
            provider=merchant.provider,
            selling_price=product_variants[0].selling_price if product_variants else Decimal('0.00'),
            stock_id=str(external_response.public_id),
            source_service=SourceService.TANDA,
        )

        external_variants_by_sku = {v.provider_sku: v for v in external_response.variants}

        for variant_data in product_variants:
            external_variant = external_variants_by_sku.get(variant_data.article)

            if not external_variant:
                continue

            variant = ProductVariant.objects.create(
                images=[urlparse(images.get(variant_data.image_id).file.url).path.lstrip("/")] if variant_data.image_id in images else [],
                product=product,
                available_quantity=external_variant.quantity or 0,
                stock_id=str(external_variant.public_id),
                cost_price=variant_data.cost_price,
                selling_price=variant_data.selling_price,
                article=variant_data.article,
                provider_sku=external_variant.provider_sku,
                sku=external_variant.sku,
                source_service=SourceService.TANDA,
            )

            for value_id in variant_data.option_value_ids:
                VariantOption.objects.create(
                    product_variant=variant,
                    option_value_id=value_id
                )

    return product


