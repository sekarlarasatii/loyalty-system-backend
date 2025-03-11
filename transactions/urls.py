from django.urls import path
from .views import SimulatePaymentView

urlpatterns = [
    path('simulate-payment/', SimulatePaymentView.as_view(), name='simulate-payment'),
]
