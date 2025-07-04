from django.db import models


class Image(models.Model):
    file = models.FileField(verbose_name="Файл", upload_to="files/%Y/%m/%d/")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
