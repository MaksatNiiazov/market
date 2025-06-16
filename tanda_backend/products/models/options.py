from django.db import models


from tanda_backend.common.models import PublicModel


class OptionType(PublicModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип опции"
        verbose_name_plural = "Типы опций"


class OptionValue(PublicModel):
    option_type = models.ForeignKey(OptionType, on_delete=models.SET_NULL, null=True)

    value = models.CharField(max_length=255)
    meta_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Значение опции"
        verbose_name_plural = "Значения опций"
