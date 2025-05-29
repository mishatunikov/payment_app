from django.urls import include, path

from api.views import ItemAPIView, StripeSessionAPIView

urlpatterns = [
    path('v1/item/<int:pk>/', ItemAPIView.as_view()),
    path('v1/buy/<int:pk>/', StripeSessionAPIView.as_view()),
]
