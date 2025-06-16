from urllib.parse import urlparse

from django.db import models

from tanda_backend.common.models import PublicModel


class Merchant(PublicModel):
    user = models.OneToOneField("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.OneToOneField("merchant.Provider", on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    document = models.FileField(null=True, blank=True, upload_to="tanda/files/%Y/%m/%d/")
    account_number = models.CharField(max_length=255, null=True, blank=True)

    birthday = models.DateField(null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    address_of_residence = models.CharField(max_length=255, null=True, blank=True)
    inn = models.CharField(max_length=255, null=True, blank=True)
    id_passport = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Мерчант"
        verbose_name_plural = "Мерчанты"

    def get_json(self):
        return {
            "merchant_id": str(self.public_id),
            "user_id": str(self.user.sso_id) if self.user else None,
            "name": self.name,
            "phone_number": self.phone_number,
            "address": self.address,
            "document": urlparse(self.document.url).path.lstrip("/") if self.document else None,
            "account_number": self.account_number,
            "birthday": str(self.birthday),
            "telegram": self.telegram,
            "address_of_residence": self.address_of_residence,
            "additional_info": self.additional_info,
            "fio": self.user.fio if self.user else None,
            "is_active": self.is_active,
            "is_approved": self.is_approved,
            "provider_id": str(self.provider.public_id) if self.provider else None
        }

    def __str__(self):
        return self.name


class Provider(PublicModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Провайдер"
        verbose_name_plural = "Провайдеры"

    def __str__(self):
        return self.name
