from django import forms
from django.forms.models import ModelForm
from .models import Offer_Details


class Project_Submit_Form(ModelForm):
    Proof_Url = forms.URLField(required=True, label="Paste Link Here(if any)", widget=forms.URLInput(attrs={"class":"Input_Url","placeholder":"Paste Link Here(if any)","style":"padding: 20px 40px;"}))
    Proof_Url_Scnd = forms.URLField(required=False, label="Paste Link Here(if any)", widget=forms.URLInput(attrs={"class":"Input_Url","placeholder":"Paste Link Here(if any)","style":"padding: 20px 40px;"}))
    Proof_Url_Third = forms.URLField(required=False, label="Paste Link Here(if any)", widget=forms.URLInput(attrs={"class":"Input_Url","placeholder":"Paste Link Here(if any)","style":"padding: 20px 40px;"}))

    class Meta:
        model = Offer_Details
        fields = ("Proof_Url","Proof_Url_Scnd","Proof_Url_Third",)
        label = {

			"Proof_Url": "Paste Link Here(if any)",

		}
