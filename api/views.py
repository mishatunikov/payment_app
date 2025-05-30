from typing import Union

import stripe
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from config import config
from items.models import Item, Order


class ItemAPIView(APIView):
    """
    Returns an HTML payment form with item details.
    """

    renderer_classes = [
        TemplateHTMLRenderer,
    ]
    template_name = 'payment_form_item.html'

    def get(self, request, pk):
        instance = get_object_or_404(Item, pk=pk)
        return Response(
            {
                'instance': instance,
                'published_key': config.stripe.published_key,
            }
        )


class OrderApiView(APIView):
    """
    Returns an HTML payment form with order details.
    """

    renderer_classes = [
        TemplateHTMLRenderer,
    ]
    template_name = 'payment_form_order.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return Response(
            {
                'items': order.items.all(),
                'published_key': config.stripe.published_key,
                'order_id': pk,
            }
        )


class StripeSessionMixin:
    """
    StripeSession mixin.

    Have a static method, which create and return checkout.Session.
    """

    @staticmethod
    def get_session(
        items: Union[QuerySet[Item], Item],
        success_url: str,
        cancel_url: str,
        discounts: Union[None, list] = None,
        taxes: Union[None, list[str]] = None,
    ) -> stripe.checkout.Session:
        """
        Create a Stripe Checkout Session for the given item(s).

        Args:
            items (Model instance or QuerySet): Single item or multiple items
            to include in the session.
            success_url (str): URL to redirect to upon successful payment.
            cancel_url (str): URL to redirect to if the payment is canceled.
            discounts (list of stripe_id or None): Stripe id of discount
                objects.
            taxes (list of stripe_id or None): Stripe id of tax
                objects.

        Returns:
            stripe.checkout.Session: The created Stripe Checkout Session
            object.
        """
        stripe_discounts = []
        stripe_taxes = []

        if discounts:
            stripe_discounts = [{'coupon': d} for d in discounts]

        if taxes:
            stripe_taxes.extend(taxes)

        stripe.api_key = config.stripe.secret_key

        if not isinstance(items, QuerySet):
            items = [items]

        line_items = [
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': int(obj.price * 100),
                    'product_data': {
                        'name': obj.name,
                        'description': obj.description,
                    },
                },
                'quantity': getattr(obj, 'quantity', 1),
                'tax_rates': stripe_taxes,
            }
            for obj in items
        ]
        return stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
            discounts=stripe_discounts,
        )


class BuyItemView(APIView, StripeSessionMixin):
    """
    API endpoint to create a Stripe Checkout Session for a single item.
    """

    def get(self, request, pk):
        instance = get_object_or_404(Item, pk=pk)
        session = self.get_session(
            instance,
            success_url='http://localhost:8000/api/v1/item/{}/'.format(pk),
            cancel_url='http://localhost:8000/api/v1/item/{}/'.format(pk),
        )
        return Response(
            {'id': session.id},
        )


class MakeOrderView(APIView, StripeSessionMixin):
    """
    API endpoint to create a Stripe Checkout Session for a full order.
    """

    def get(self, request, pk):
        instance = get_object_or_404(Order, pk=pk)
        session = self.get_session(
            instance.items.all(),
            success_url=f'{config.host.domain_name}/api/v1/order/{pk}/',
            cancel_url=f'{config.host.domain_name}/api/v1/order/{pk}/',
            discounts=list(
                instance.discounts.values_list('stripe_id', flat=True)
            ),
            taxes=list(instance.taxes.values_list('stripe_id', flat=True)),
        )
        return Response(
            {'id': session.id},
        )
