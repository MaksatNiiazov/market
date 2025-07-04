from django.contrib import admin
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings
from mptt.admin import DraggableMPTTAdmin

from tanda_backend.products.models import Category, CategoryOptionRequirement, OptionType, OptionValue, Product
from tanda_backend.products.services.category_option_events import (
    send_option_type_created_event, send_option_type_updated_event, send_option_type_deleted_event,
    send_option_value_created_event, send_option_value_updated_event, send_option_value_deleted_event,
    send_category_created_event, send_category_updated_event, send_category_deleted_event,
    send_category_option_requirement_created_event, send_category_option_requirement_updated_event,
    send_category_option_requirement_deleted_event
)


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    if created:
        send_category_created_event(instance)
    else:
        send_category_updated_event(instance)


@receiver(pre_delete, sender=Category)
def category_pre_delete(sender, instance, **kwargs):
    send_category_deleted_event(str(instance.public_id))


class CategoryOptionRequirementInline(admin.TabularInline):
    model = CategoryOptionRequirement
    extra = 1
    fields = ('option_type', 'is_main', 'is_required', 'sort_order')


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'show_option_requirements')
    list_display_links = ('indented_title',)
    inlines = [CategoryOptionRequirementInline]

    def get_form(self, request, obj=None, **kwargs):
        request._obj = obj
        return super().get_form(request, obj, **kwargs)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            is_new = not instance.pk
            instance.save()
            if is_new:
                send_category_option_requirement_created_event(instance)
            else:
                send_category_option_requirement_updated_event(instance)

        for obj in formset.deleted_objects:
            if isinstance(obj, CategoryOptionRequirement):
                public_id = str(obj.public_id)
                obj.delete()
                send_category_option_requirement_deleted_event(public_id)

        formset.save_m2m()

    def show_option_requirements(self, obj):
        requirements = CategoryOptionRequirement.objects.filter(category=obj)
        if not requirements.exists():
            return "-"

        requirements_list = [f"{req.option_type.name} ({'Основная' if req.is_main else 'Дополнительная'}, {'Обязательная' if req.is_required else 'Необязательная'})"
                             for req in requirements]
        return format_html('<br>'.join(requirements_list))

    show_option_requirements.short_description = "Требования опций"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}

        if obj:
            ancestors = obj.get_ancestors()

            parent_requirements = []
            for ancestor in ancestors:
                reqs = CategoryOptionRequirement.objects.filter(category=ancestor)
                for req in reqs:
                    parent_requirements.append({
                        'category': ancestor.name,
                        'option_type': req.option_type.name,
                        'is_main': req.is_main,
                        'is_required': req.is_required,
                        'sort_order': req.sort_order
                    })

            extra_context['parent_requirements'] = parent_requirements

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class OptionValueInline(admin.TabularInline):
    model = OptionValue
    extra = 1
    fields = ('value', 'meta_data')


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    inlines = [OptionValueInline]

    def save_model(self, request, obj, form, change):
        is_new = not obj.pk
        super().save_model(request, obj, form, change)

        if is_new:
            send_option_type_created_event(obj)
        else:
            send_option_type_updated_event(obj)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            is_new = not instance.pk
            instance.save()
            if is_new:
                send_option_value_created_event(instance)
            else:
                send_option_value_updated_event(instance)

        for obj in formset.deleted_objects:
            public_id = str(obj.public_id)
            obj.delete()
            send_option_value_deleted_event(public_id)

        formset.save_m2m()

    def delete_model(self, request, obj):
        option_values = list(obj.optionvalue_set.all())
        option_value_public_ids = [str(value.public_id) for value in option_values]

        public_id = str(obj.public_id)
        super().delete_model(request, obj)

        for value_public_id in option_value_public_ids:
            send_option_value_deleted_event(value_public_id)

        send_option_type_deleted_event(public_id)

    def delete_queryset(self, request, queryset):
        all_option_value_public_ids = []
        for obj in queryset:
            option_values = list(obj.optionvalue_set.all())
            all_option_value_public_ids.extend([str(value.public_id) for value in option_values])

        public_ids = [str(obj.public_id) for obj in queryset]
        super().delete_queryset(request, queryset)

        for value_public_id in all_option_value_public_ids:
            send_option_value_deleted_event(value_public_id)

        for public_id in public_ids:
            send_option_type_deleted_event(public_id)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('linked_title', 'show_thumbnail', 'category', 'brand', 'merchant', 'provider', 'selling_price', 'is_approved', 'variants_count')
    list_filter = ('is_approved', 'category', 'merchant', 'provider', 'brand')
    search_fields = ('title', 'description', 'stock_id', 'brand')
    readonly_fields = ('title', 'description', 'slug', 'brand', 'stock_id', 'category', 'group_by_option_id', 'merchant', 'provider', 'images', 'show_images', 'variants_display')
    actions = ['approve_products', 'unapprove_products']
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', "images", "show_images", 'description', 'slug', 'brand', 'stock_id', 'selling_price', 'is_approved')
        }),
        ('Связи', {
            'fields': ('category', 'group_by_option_id', 'merchant', 'provider')
        }),
        ('Варианты товара', {
            'fields': ('variants_display',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Если это создание нового объекта, не делаем поля только для чтения
        if obj is None:
            return ('show_images', 'variants_display')
        return self.readonly_fields

    def linked_title(self, obj):
        url = reverse('admin:products_product_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.title)
    linked_title.short_description = "Название товара"

    def show_thumbnail(self, obj):
        cdn_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '')

        if obj.images and len(obj.images) > 0:
            img_url = f"https://{cdn_domain}/{obj.images[0]}" if cdn_domain else obj.images[0]
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', img_url)
        return "-"
    show_thumbnail.short_description = "Фото"

    def show_images(self, obj):
        if not obj.images or len(obj.images) == 0:
            return "-"

        # Get CDN domain from settings
        cdn_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '')

        html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
        for img in obj.images:
            # Prepend CDN domain to image path
            img_url = f"https://{cdn_domain}/{img}" if cdn_domain else img
            html += f'<img src="{img_url}" width="150" height="150" style="object-fit: cover;" />'
        html += '</div>'
        return format_html(html)

    show_images.short_description = "Галерея изображений"

    def variants_count(self, obj):
        return obj.productvariant_set.count()
    variants_count.short_description = "Кол-во вариантов"

    def variants_display(self, obj):
        variants = obj.productvariant_set.all()
        if not variants:
            return "Нет вариантов товара"

        cdn_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '')

        html = '<div style="margin-bottom: 20px;">'
        for variant in variants:
            html += f'<div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">'
            html += f'<h3>Артикул: {variant.article or "Не указан"}</h3>'
            html += f'<p>ID: {variant.id}, Stock ID: {variant.stock_id}</p>'
            html += f'<p>Доступное количество: {variant.available_quantity}</p>'
            html += f'<p>Цена закупки: {variant.cost_price} | Цена продажи: {variant.selling_price}</p>'

            # Отображаем опции варианта
            options = variant.variantoption_set.all()
            if options:
                html += '<div style="margin: 10px 0;"><strong>Опции:</strong><ul>'
                for option in options:
                    if option.option_value:
                        html += f'<li>{option.option_value.option_type.name}: {option.option_value.value}</li>'
                html += '</ul></div>'

            # Отображаем изображения варианта
            if variant.images and len(variant.images) > 0:
                html += '<div style="margin-top: 15px;"><strong>Фотографии варианта:</strong></div>'
                html += '<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px; background-color: #f9f9f9; padding: 10px; border-radius: 5px;">'
                for img in variant.images:
                    img_url = f"https://{cdn_domain}/{img}" if cdn_domain else img

                    html += f'<div style="position: relative;">'
                    html += f'<img src="{img_url}" width="150" height="150" style="object-fit: cover; border: 1px solid #ddd; border-radius: 3px;" />'
                    html += '</div>'
                html += '</div>'

            html += '</div>'
        html += '</div>'
        return format_html(html)
    variants_display.short_description = "Варианты товара"

    def approve_products(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'Одобрено {updated} товаров.')
    approve_products.short_description = "Одобрить выбранные товары"

    def unapprove_products(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'Отменено одобрение для {updated} товаров.')
    unapprove_products.short_description = "Отменить одобрение для выбранных товаров"

