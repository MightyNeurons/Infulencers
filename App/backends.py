from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Acount_Influencer, Influencer_Details, Usa_Tax_Payer
from django.core.mail import send_mail
from django.conf import settings
import requests


class AccountAuth(ModelBackend):

    def authenticate(Username=None, Password = None):
        UserModel = get_user_model()
        if Username is not None:
            try:
                id = UserModel.objects.all().filter(email = Username).values("id")[0]["id"]
            except:
                return None
        if id is not None:
            try:
                user_pass = UserModel.objects.all().filter(id = id).values("password")[0]['password']
                if user_pass == Password:
                    return id
            except:
                return None
        
        else:
            return None
    
    def get_user(self,id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk= id) # <-- must be primary key and number
        except User.DoesNotExist:
            return None

    def Get_Influencer_Id(Id):
        try:
            User_Login_Id = Acount_Influencer.objects.get(User = Id)
            User_Details_Id = Influencer_Details.objects.get(User = User_Login_Id)
            if User_Details_Id is not None:
                return User_Details_Id
            else:
                return None
        except:
            return None

    def Get_Urls(Recipient, Token):
        Subject = "MightyNeurons Email Verification"
        Message = f"Your Account Needs to Be Verified http://127.0.0.1:8000/Verify/{Token}"
        Email_Sender = settings.EMAIL_HOST_USER
        Email_Reciever = [Recipient]
        send_mail(subject=Subject, message=Message, from_email=Email_Sender, recipient_list=Email_Reciever)

    def Check_Phone_Number(Number):
        try:
            Check_Exsisting_Phone = Influencer_Details.objects.get(Phone_Number = Number)
            if Check_Exsisting_Phone is not None:
                return Check_Exsisting_Phone
            else:
                return None
        except:
            return None

    def Get_Status(url):
        if url is not None:
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    return "success"
                else:
                    return None
            except:
                return None
        else:
            return None

    def Get_Usa_User(uid):
        try:
            User_Country = Influencer_Details.objects.all().filter(User = uid).values("Country")[0]["Country"]
            if User_Country == "United States":
                try:
                    User_ID = Usa_Tax_Payer.objects.all().filter(User = uid).values("User")[0]["User"]
                    return None
                except:
                    return uid
            else:
                return None
        except:
            return None


