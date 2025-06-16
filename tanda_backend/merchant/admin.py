from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from tanda_backend.common.eventstore import append_to_stream, serialize
from esdbclient import NewEvent
from tanda_backend.merchant.models import Merchant, Provider


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_active', 'is_approved', 'approval_actions')
    list_filter = ('is_active', 'is_approved')
    search_fields = ('name', 'phone_number')
    readonly_fields = ('public_id',)

    def approval_actions(self, obj):
        if obj.is_approved:
            button_html = '<a class="button" href="{}" style="background-color: #FF4136; color: white;">Отменить одобрение</a>'
            return format_html(button_html, f'/admin/merchant/merchant/{obj.id}/disapprove/')
        else:
            button_html = '<a class="button" href="{}" style="background-color: #2ECC40; color: white;">Одобрить</a>'
            return format_html(button_html, f'/admin/merchant/merchant/{obj.id}/approve/')

    approval_actions.short_description = 'Действия'
    approval_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/approve/',
                self.admin_site.admin_view(self.approve_merchant),
                name='merchant-approve',
            ),
            path(
                '<path:object_id>/disapprove/',
                self.admin_site.admin_view(self.disapprove_merchant),
                name='merchant-disapprove',
            ),
        ]
        return custom_urls + urls

    def approve_merchant(self, request, object_id):
        merchant = self.get_object(request, object_id)
        merchant.is_approved = True
        merchant.save()

        event = NewEvent(
            type="MerchantApproved",
            data=serialize(merchant.get_json()),
        )
        append_to_stream(event, "merchants")

        self.message_user(request, f'Мерчант "{merchant.name}" успешно одобрен')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/merchant/merchant/'))

    def disapprove_merchant(self, request, object_id):
        merchant = self.get_object(request, object_id)
        merchant.is_approved = False
        merchant.save()

        event = NewEvent(
            type="MerchantDisapproved",
            data=serialize(merchant.get_json()),
        )
        append_to_stream(event, "merchants")

        self.message_user(request, f'Одобрение мерчанта "{merchant.name}" отменено')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/merchant/merchant/'))


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'show_merchant')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('public_id', 'show_merchant_details')
    actions = ['create_merchants']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def show_merchant(self, obj):
        try:
            merchant = Merchant.objects.get(provider=obj)
            url = reverse('admin:merchant_merchant_change', args=[merchant.id])
            return format_html('<a href="{}">{}</a>', url, merchant.name)
        except Merchant.DoesNotExist:
            url = reverse('admin:merchant_provider_create_merchant', args=[obj.id])
            return format_html('<a class="button" href="{}">Создать мерчанта</a>', url)
    show_merchant.short_description = "Мерчант"

    def show_merchant_details(self, obj):
        try:
            merchant = Merchant.objects.get(provider=obj)
            url = reverse('admin:merchant_merchant_change', args=[merchant.id])
            html = f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">' \
                   f'<h3>Мерчант: <a href="{url}">{merchant.name}</a></h3>' \
                   f'<p>Активен: {"Да" if merchant.is_active else "Нет"}</p>' \
                   f'<p>Одобрен: {"Да" if merchant.is_approved else "Нет"}</p>'

            if merchant.user:
                html += f'<p>Пользователь: {merchant.user.username}</p>'

            html += '</div>'
            return format_html(html)
        except Merchant.DoesNotExist:
            url = reverse('admin:merchant_provider_create_merchant', args=[obj.id])
            return format_html('<a class="button" href="{}">Создать мерчанта</a>', url)
    show_merchant_details.short_description = "Детали мерчанта"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/create-merchant/',
                self.admin_site.admin_view(self.create_merchant_view),
                name='merchant_provider_create_merchant',
            ),
        ]
        return custom_urls + urls

    def create_merchant_view(self, request, object_id):
        provider = self.get_object(request, object_id)
        if not provider:
            return HttpResponseRedirect(reverse('admin:merchant_provider_changelist'))

        try:
            merchant = Merchant.objects.get(provider=provider)
            self.message_user(request, f'Мерчант для провайдера "{provider.name}" уже существует', level=messages.WARNING)
            return HttpResponseRedirect(reverse('admin:merchant_merchant_change', args=[merchant.id]))
        except Merchant.DoesNotExist:
            pass

        merchant = Merchant.objects.create(
            name=provider.name,
            provider=provider,
            is_active=provider.is_active,
            is_approved=False
        )

        self.message_user(request, f'Мерчант "{merchant.name}" успешно создан')
        return HttpResponseRedirect(reverse('admin:merchant_merchant_change', args=[merchant.id]))

    def create_merchants(self, request, queryset):
        created_count = 0
        already_exists_count = 0

        for provider in queryset:
            try:
                Merchant.objects.get(provider=provider)
                already_exists_count += 1
            except Merchant.DoesNotExist:
                Merchant.objects.create(
                    name=provider.name,
                    provider=provider,
                    is_active=provider.is_active,
                    is_approved=False
                )
                created_count += 1

        if created_count > 0:
            self.message_user(request, f'Создано {created_count} новых мерчантов')
        if already_exists_count > 0:
            self.message_user(request, f'Для {already_exists_count} провайдеров мерчанты уже существуют', level=messages.WARNING)
    create_merchants.short_description = "Создать мерчантов для выбранных провайдеров"
