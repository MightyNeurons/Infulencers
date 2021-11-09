from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("<id>", views.Checkout, name="Checkout"),
    path("Checkout_Pay/<id>", views.Checkout_Pay, name="Checkout_Pay"),
    path('Completeorder',views.Completeorder,name='Completeorder'),
]