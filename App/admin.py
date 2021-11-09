from django.contrib import admin
from .models import Account, Acount_Influencer, Influencer_Details, Instagram_Account_Details,Youtube_Account_Details,Usa_Tax_Payer

# Register your models here.

admin.site.register(Account)
admin.site.register(Acount_Influencer)
admin.site.register(Influencer_Details)
admin.site.register(Instagram_Account_Details)
admin.site.register(Youtube_Account_Details)
admin.site.register(Usa_Tax_Payer)