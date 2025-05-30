import stripe
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from config import config
from items.models import Discount, Tax

stripe.api_key = config.stripe.secret_key


@receiver(post_save, sender=Discount)
def create_stripe_coupon(sender, instance: Discount, created, **kwargs):
    if created and not instance.stripe_id:
        coupon = stripe.Coupon.create(
            percent_off=instance.percent_off,
            duration='once',
            name=instance.name,
        )
        instance.stripe_id = coupon.id
        instance.save()


@receiver(post_save, sender=Tax)
def create_stripe_tax(sender, instance, created, **kwargs):
    if created and not instance.stripe_id:
        tax = stripe.TaxRate.create(
            display_name=instance.name,
            description=instance.__str__(),
            percentage=instance.percentage,
            inclusive=False,
        )
        instance.stripe_id = tax.id
        instance.save()
