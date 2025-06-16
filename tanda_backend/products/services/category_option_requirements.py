from tanda_backend.products.models import Category, CategoryOptionRequirement


def get_option_requirements_by_category(category_id: int):
    category = Category.objects.get(id=category_id)
    ancestor_ids = list(category.get_ancestors(include_self=True).values_list('id', flat=True))
    options = CategoryOptionRequirement.objects.filter(
        category_id__in=ancestor_ids
    ).select_related('option_type').order_by("option_type").distinct("option_type")
    return options


def get_main_option_by_category(category_id: int):
    category = Category.objects.get(id=category_id)
    ancestor_ids = list(category.get_ancestors(include_self=True).values_list('id', flat=True))
    option = CategoryOptionRequirement.objects.filter(
        category_id__in=ancestor_ids,
        is_main=True,
    ).order_by('sort_order').distinct().first()
    return option
