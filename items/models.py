from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from items import consts


class BaseName(models.Model):
    """Abstract model with name field."""

    name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, unique=True, verbose_name='название'
    )

    class Meta:
        abstract = True
        ordering = ('name',)


class TaxDiscountBase(BaseName):
    """Abstract model with stripe_id and name fields."""

    stripe_id = models.CharField(
        max_length=consts.STRIPE_ID_MAX_LENGTH,
        blank=True,
        null=True,
    )

    class Meta(BaseName.Meta):
        abstract = True


class Item(BaseName):
    """Item model."""

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

    class Meta(BaseName.Meta):
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order model."""

    items = models.ManyToManyField(
        Item, related_name='orders', verbose_name='товары'
    )
    discounts = models.ManyToManyField(
        'Discount', blank=True, related_name='orders', verbose_name='скидки'
    )
    taxes = models.ManyToManyField(
        'Tax', blank=True, related_name='orders', verbose_name='налоги'
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


class Discount(TaxDiscountBase):
    """Discount model"""

    percent_off = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(consts.MIN_DISCOUNT_PERCENT),
            MaxValueValidator(consts.MAX_DISCOUNT_PERCENT),
        ],
        verbose_name='процент скидки',
    )

    class Meta(TaxDiscountBase.Meta):
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    def __str__(self):
        return f'{self.name} ({self.percent_off}%)'


class Tax(TaxDiscountBase):
    """Tax model."""

    percentage = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(consts.MIN_TAX_PERCENT)],
        verbose_name='процент налога',
    )

    class Meta(TaxDiscountBase.Meta):
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'

    def __str__(self):
        return f'{self.name} ({self.percentage}%)'
