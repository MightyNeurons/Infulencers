from django.db import models

# Create your models here.

class Offer_Details(models.Model):
    Proof_Url = models.URLField()
    Proof_Url_Scnd = models.URLField(blank=True)
    Proof_Url_Third = models.URLField(blank=True)


