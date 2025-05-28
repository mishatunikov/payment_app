from django.urls import include, path

from api.views import ItemAPIView

urlpatterns = [
    path('v1/item/<int:pk>/', ItemAPIView.as_view()),
]
