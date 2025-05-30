from django.urls import include, path

from api.views import BuyItemView, ItemAPIView, MakeOrderView, OrderApiView

urlpatterns = [
    path('v1/item/<int:pk>/', ItemAPIView.as_view()),
    path('v1/buy/<int:pk>/', BuyItemView.as_view()),
    path('v1/order/<int:pk>/', OrderApiView.as_view()),
    path('v1/order/<int:pk>/payment/', MakeOrderView.as_view()),
]
