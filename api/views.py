from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from items.models import Item


class ItemAPIView(APIView):
    """
    Returns an HTML payment form with item details rendered f
    rom 'payment_form.html'.
    """

    renderer_classes = [TemplateHTMLRenderer,]
    template_name = 'payment_form.html'

    def get(self, request, pk):
        instance = get_object_or_404(Item, pk=pk)
        return Response({'instance': instance})
