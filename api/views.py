import stripe
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from config import config
from items.models import Item


class ItemAPIView(APIView):
    """
    Returns an HTML payment form with item details rendered f
    rom 'payment_form.html'.
    """

    renderer_classes = [
        TemplateHTMLRenderer,
    ]
    template_name = 'payment_form.html'

    def get(self, request, pk):
        instance = get_object_or_404(Item, pk=pk)
        return Response(
            {
                'instance': instance,
                'published_key': config.stripe.published_key,
            }
        )


class StripeSessionAPIView(APIView):
    """
    Returns a Stripe session id.
    """

    def get(self, request, pk):
        instance = get_object_or_404(Item, pk=pk)
        stripe.api_key = config.stripe.secret_key
        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'rub',
                        'unit_amount': int(instance.price * 100),
                        'product_data': {
                            'name': instance.name,
                            'description': instance.description,
                        },
                    },
                    'quantity': 1,
                }
            ],
            success_url='http://localhost:8000/api/v1/item/{}/'.format(
                instance.pk
            ),
            cancel_url='http://localhost:8000/api/v1/item/{}/'.format(
                instance.pk
            ),
        )

        return Response(
            {'id': session.id},
        )
