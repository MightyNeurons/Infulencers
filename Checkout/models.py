from django.db import models

# Create your models here.
class Buyers(models.Model):
    Fullname = models.CharField(max_length=200, null=True)
    organization = models.CharField(max_length=200, null=True)
    Billing_Addresss = models.CharField(max_length=500, null=True)
    Bill_Number = models.BigAutoField(primary_key=True)
    User = models.IntegerField()
    Date_Created = models.DateField(auto_now_add=True)


class Checkout_Data(models.Model):
    User_id = models.IntegerField()
    Ordered_Product = models.CharField(max_length=20)
    Order_Product_Type = models.CharField(max_length=100)


class Notification_Data(models.Model):
    Sender_id = models.IntegerField()
    Receiver_id = models.IntegerField(blank=True,default=999999999)
    Topic = models.CharField(max_length=200)
    Date_Created = models.DateField(auto_now_add=True)
    Type = models.CharField(max_length=20,default="N/A")
    Gig_Id = models.IntegerField(blank=True, default=999999999)

class Project_Creation(models.Model):
    Created_For = models.IntegerField()
    Created_By = models.IntegerField()
    Product_Id = models.IntegerField()
    Product_Type = models.CharField(max_length=20)
    is_Completed = models.BooleanField(default=False)
    Payment_Made = models.BooleanField(default=False)
    Payment_Released = models.BooleanField(default=False)
    Is_Proof_Url = models.BooleanField(default=False)
    Is_Delivery_Time = models.BooleanField(default=False)
    Is_Pyament_Released = models.BooleanField(default=False)
    Is_Payment_peding = models.BooleanField(default=True)
    Is_Disputed = models.BooleanField(default=False)
    Is_Realesed_Requested = models.BooleanField(default=False)
    Date_Created = models.DateField(auto_now_add=True)
    

