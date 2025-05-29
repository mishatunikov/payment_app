from django.core.validators import MinValueValidator
from django.db import models

from items import consts


class Item(models.Model):
    name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, unique=True, verbose_name='название'
    )
    description = models.TextField(
        max_length=consts.MAX_TEXT_LENGTH, verbose_name='описание'
    )
    price = models.DecimalField(
        max_digits=consts.MAX_DIGITS_DECIMAL,
        decimal_places=consts.DECIMAL_PLACES,
        validators=[
            MinValueValidator(consts.MIN_PRICE),
        ],
        verbose_name='цена',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(
        Item, related_name='orders', verbose_name='товары'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Заказ №{self.pk}'
