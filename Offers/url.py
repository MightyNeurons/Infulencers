from django.urls import path
from . import views





urlpatterns = [
    path("<id>", views.Offer, name="Offers"),
    path("ReleasePayment",views.ReleasePayment, name='ReleasePayment'),
]