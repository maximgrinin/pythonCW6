from django.conf import settings
from django.db import models


class Ad(models.Model):
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Фото",
        help_text="Прикрепите фото к объявлению",
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="Введите название товара",
    )

    price = models.PositiveIntegerField(
        verbose_name="Цена товара",
        help_text="Введите цену товара"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор объявления",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания объявления",
    )

    description = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name="Описание товара",
        help_text="Введите описание товара"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ("-created_at",)


class Comment(models.Model):
    text = models.CharField(
        max_length=1000,
        verbose_name="Комментарий",
        help_text="Оставьте свой комментарий здесь",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания комментария",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )

    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Объявление",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-created_at",)
