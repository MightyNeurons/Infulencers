from typing import Counter
from django import forms
from django.forms.models import ModelForm



class buyersform(forms.Form):
    Fullname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={"placeholder":"Fullname"}))
    Organization = forms.CharField(required=False, max_length= 200,widget=forms.TextInput(attrs={"placeholder":"Organization(optional)"}))
    Billing_Address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"placeholder":"Please enter Address with Zip"}))