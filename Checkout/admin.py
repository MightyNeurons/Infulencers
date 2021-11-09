from django.contrib import admin
from .models import Buyers, Checkout_Data, Notification_Data

# Register your models here.
admin.site.register(Checkout_Data)
admin.site.register(Buyers)
admin.site.register(Notification_Data)