from django.db import models

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from tanda_backend.common.models import PublicModel


class Category(MPTTModel, PublicModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CategoryOptionRequirement(PublicModel):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    option_type = models.ForeignKey("OptionType", on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    is_required = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.category.name} {self.option_type.name}"

    class Meta:
        verbose_name = "Обязательная опция категория"
        verbose_name_plural = "Обязательные опции категорий"
