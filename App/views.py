from django.contrib.auth.models import User
from django.http import request
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .form import Register_Forms, AccountAuthenticationForm, Is_Influencer_Form,Details_Inf, OTP_form, USA_W_Nine_Form, Create_Gig_Form_Initial, Create_Gig_Form_Pkg,Create_Gig_Form_Describe, Create_Gig_Form_Attachment
from django.contrib.auth import  get_user_model, login, logout
from .models import Acount_Influencer, Account, Influencer_Details, Instagram_Account_Details, Youtube_Account_Details, Usa_Tax_Payer, Gigs, Gig_Attachments, Initial_Data, Pkg_Form_Data, Describe_Gig
from .backends import AccountAuth
import datetime
import json
import random
from django.contrib import messages
import http.client
from django.conf import settings
from twilio.rest import Client
from django.template.defaultfilters import slugify
from .Scrapper_Bots.Instagram_Bot import Insta_Bot
from .Scrapper_Bots.YoutubeBot import Youtube_bot
from time import time, sleep
from apscheduler.schedulers.background import BackgroundScheduler
from ipware import get_client_ip
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from formtools.wizard.views import SessionWizardView
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.core.files.images import get_image_dimensions
from notifications.signals import notify
from Checkout.models import Project_Creation
from .Utility import Get_Project_Id, Get_Recipent_User
from Checkout.models import Notification_Data

# Create your views here.


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,"about.html")


def Registrations(request):
    context = {}
    if request.POST:
        forms = Register_Forms(request.POST)
        if forms.is_valid():
            forms.save()
            user_email = forms.cleaned_data["email"]
            Is_Verified = Account.objects.all().filter(email = user_email).values("is_email_varified")[0]["is_email_varified"]
            if Is_Verified==False:
                Uuid = Account.objects.all().filter(email = user_email).values("UUid_Token")[0]['UUid_Token']
                AccountAuth.Get_Urls(Recipient=user_email,Token=Uuid)
                return redirect('/Mail_Sent')
            else:
                return redirect("/Login")
        else:
            context['Registration_Form'] = forms
            return render(request, 'sign-up.html', context)
    else:
        forms = Register_Forms()
        context['Registration_Form'] = forms
    return render(request, 'sign-up.html', context)


def Mail_Sent(request):
    return render(request,"Sent_Email.html")


def Login(request):
    if request.method == "POST":
        Login_form = AccountAuthenticationForm(request.POST)
        if Login_form.is_valid():
            user_email = Login_form.cleaned_data["email"]
            user_password = Login_form.cleaned_data["password"]
            user = AccountAuth.authenticate(Username= user_email, Password= user_password)
            if user is not None:
                user_model = get_user_model()
                user_profile = user_model.objects.get(id = user)
                if user_profile.is_active:
                    Is_Verified = Account.objects.all().filter(id = user).values("is_email_varified")[0]["is_email_varified"]
                    if Is_Verified == True:
                        request.session['uid'] = user_email
                        login(request,user_profile, backend='App.backends.AccountAuth')
                        User_Login_Id = AccountAuth.Get_Influencer_Id(user)
                        if User_Login_Id is not None:
                            return redirect('index')
                        else:
                            return redirect('/Is_Influencer')
                    else:
                        Uuid = Account.objects.all().filter(id = user).values("UUid_Token")[0]['UUid_Token']
                        AccountAuth.Get_Urls(Recipient=user_email,Token=Uuid)
                        messages.success(request,"An Email has been Sent to You")
                        Login_form = AccountAuthenticationForm()
                        return render(request,"sign-in.html",{"Login":Login_form})
            else:
                Login_form = AccountAuthenticationForm()
                return render(request,"sign-in.html",{"Login":Login_form,"Details":"User Name or Password is not Correct"})
    else:
        Login_form = AccountAuthenticationForm()

    return render(request,"sign-in.html",{"Login":Login_form})

def Verify(request, Token):
    try:
        Profile_Obj = Account.objects.all().filter(UUid_Token = Token).first()
        if Profile_Obj:
            Account.objects.all().filter(UUid_Token = Token).update(is_email_varified = True)
            messages.success(request,"Your Account has been Verified")
            return redirect("/Login")
    except Exception as e:
        print(e)

def Logout(request):
    #del request.session['uid']
    logout(request=request)
    return redirect("/Login")


def Is_Influencer(request):
    try:
        User_Id = request.user.id
        Is_Id_Present = Acount_Influencer.objects.get(User = User_Id)
        if Is_Id_Present is not None:
            return redirect("/Details_Influencer")
    except:
        if request.method == "POST":
            Influencer_Form = Is_Influencer_Form(request.POST)
            if Influencer_Form.is_valid():
                Is_Inf = Influencer_Form.cleaned_data["Is_Influencer"]
                Is_Hiring = Influencer_Form.cleaned_data["Is_Hiring_Influencer"]
                Id = request.user.id
                if Is_Inf == True and Is_Hiring == True:
                    messages.error(request,"Please Select One")
                    return render(request,"sign-middle-Influencer.html",{"Inf":Influencer_Form})
                else:
                    Data = Acount_Influencer(User = Id, Is_Influencer = Is_Inf,Is_Hiring_Influencer = Is_Hiring )
                    Data.save()
                    user_id = request.user.id
                    Is_Influencers = Acount_Influencer.objects.all().filter(User = user_id).values("Is_Influencer")[0]["Is_Influencer"]
                    if Is_Influencers == True:
                        return redirect("/Welcome_Influencer")
                    else:
                        return redirect("/Welcome_Hiring_Manager")
            else:
                Influencer_Form = Is_Influencer_Form()
                return render(request,"sign-middle-Influencer.html",{"Inf":Influencer_Form})
        else:
            Influencer_Form = Is_Influencer_Form()
            return render(request,"sign-middle-Influencer.html",{"Inf":Influencer_Form})



def Welcome_Influencer(request):
    return render(request,"Welcome.html")

def Welcome_Hiring_Manager(request):
    return render(request,"Welcome.html")

def Details_Influencer(request):
    User_Id = request.user.id
    try:
        Details_Id = Influencer_Details.objects.get(User = User_Id)
        User_Name = Influencer_Details.objects.all().filter(User = User_Id).values("Slug_Name")[0]["Slug_Name"]
        Phone_Verified = Influencer_Details.objects.all().filter(User = User_Id).values("Is_Phone_Verified")[0]["Is_Phone_Verified"]
        Phone = Influencer_Details.objects.all().filter(User = User_Id).values("Phone_Number")[0]["Phone_Number"]
        Otp = Influencer_Details.objects.all().filter(User = User_Id).values("Otp")[0]["Otp"]
        if Details_Id is not None:
            if Phone_Verified:
                return redirect("Dashboard/{}".format(User_Name))
            else:
                SID = settings.AUTH_SID
                Auth_Key = settings.AUTH_KEY
                client = Client(SID,Auth_Key)
                Msg = "OTP to Verify Your Phone Number is {}"
                Bdy_Msg = Msg.format(Otp)
                try:
                    client.messages.create(to=Phone,body= Bdy_Msg,from_='+19548330030')
                    return redirect("/otp")
                except:
                    return HttpResponseBadRequest()
        else:
            return Http404()
    except:
        if request.method == "POST":
            Details_Form = Details_Inf(request.POST,request.FILES)
            if Details_Form.is_valid():
                First  = Details_Form.cleaned_data["First_Name"]
                Last  = Details_Form.cleaned_data["Last_Name"]
                Picture = request.FILES["Profile_Picture"]
                Des = Details_Form.cleaned_data["Descriptions"]
                Aud = Details_Form.cleaned_data["Audience"]
                Cnt = Details_Form.cleaned_data["Country"]
                Tiktok = Details_Form.cleaned_data["Tiktok_Link"]
                Instagram = Details_Form.cleaned_data["Instagram_Link"]
                Youtube = Details_Form.cleaned_data["Youtube_Link"]
                Phone = Details_Form.cleaned_data["Phone_Number"]
                Slug_Field = slugify(str(First+Last))
                otp = random.randint(1000, 9000)
                Data = Influencer_Details(First_Name = First,Last_Name = Last,Profile_Picture = Picture, Descriptions = Des, Audience = Aud , Country = Cnt, Tiktok_Link = Tiktok,Instagram_Link = Instagram,Youtube_Link = Youtube, Phone_Number = Phone,User = request.user.id, Otp = otp, Slug_Name = Slug_Field)
                Does_Exists = AccountAuth.Check_Phone_Number(Phone)
                Status_Tiktok = AccountAuth.Get_Status(Tiktok)
                Status_Youtube = AccountAuth.Get_Status(Youtube)
                Status_Insta = AccountAuth.Get_Status(Instagram)
                if Does_Exists is not None:
                    Error_Phone_Exist = "This Mobile Number is Already Exist"
                    return render(request,"sign-middle-Influencer-Preference.html",{"Details_Infs":Details_Form,"Exist":Error_Phone_Exist})
                elif Status_Tiktok is None and Status_Youtube is None and Status_Insta is None:
                    Error_Links = "Please Enter Atleast One Valid Social Profile Link"
                    return render(request,"sign-middle-Influencer-Preference.html",{"Details_Infs":Details_Form,"Exist":Error_Links})
                else:
                    Send_Otp(mobile=str(Phone),Otp= otp,Data_Model=Data)
                    return redirect("/otp")
                    
            else:
                Details_Form = Details_Inf()
                return render(request,"sign-middle-Influencer-Preference.html",{"Details_Infs":Details_Form,"Exist":"Somthing Went Wrong, Please Provide Valid details"})
        else:
            Details_Form = Details_Inf()
        return render(request,"sign-middle-Influencer-Preference.html",{"Details_Infs":Details_Form})




def Send_Otp(mobile , Otp, Data_Model):
    SID = settings.AUTH_SID
    Auth_Key = settings.AUTH_KEY
    client = Client(SID,Auth_Key)
    Msg = "OTP to Verify Your Phone Number is {}"
    Bdy_Msg = Msg.format(Otp)
    try:
        client.messages.create(to=mobile,body= Bdy_Msg,from_='+19548330030')
        Data_Model.save()
    except:
        return redirect("index")

def otp(request):
    if request.method == "POST":
        Otp_Forms= OTP_form(request.POST)
        if Otp_Forms.is_valid():
            user_id = request.user.id
            OTP_Verify = Influencer_Details.objects.all().filter(User = user_id).values("Otp")[0]["Otp"]
            Otp_Entered = Otp_Forms.cleaned_data["Otp"]
            if OTP_Verify == Otp_Entered:
                Influencer_Details.objects.all().filter(User = user_id).update(Is_Phone_Verified = True)
                User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
                User_Ids = AccountAuth.Get_Usa_User(uid=user_id)
                if User_Ids is not None:
                    return redirect("/UsaTaxForm")
                else:
                    return redirect("Dashboard/{}".format(User_Name))
            else:
                messages.error(request,"Wrong OTP")
                return render(request,"OTP.html",{"OTP_FORM":Otp_Forms})
        else:
            Otp_Forms= OTP_form()
            return render(request,"OTP.html",{"OTP_FORM":Otp_Forms})
    else:
        Otp_Forms= OTP_form()
    return render(request,"OTP.html",{"OTP_FORM":Otp_Forms})

def UsaTaxForm(request):
    if request.method == "POST":
        W_Nine_Form = USA_W_Nine_Form(request.POST)
        if W_Nine_Form.is_valid():
            User_Name = W_Nine_Form.cleaned_data["Name"]
            Business = W_Nine_Form.cleaned_data["Business_Name"]
            Federal_tax = W_Nine_Form.cleaned_data["Federal_tax_classification"]
            Exempt_payee = W_Nine_Form.cleaned_data["Exempt_payee_code"]
            Exempt_FATCA = W_Nine_Form.cleaned_data["Exempt_FATCA_code"]
            Address = W_Nine_Form.cleaned_data["Address"]
            City = W_Nine_Form.cleaned_data["City"]
            State = W_Nine_Form.cleaned_data["State"]
            Zip = W_Nine_Form.cleaned_data["Zip_Code"]
            Social_security = W_Nine_Form.cleaned_data["Social_security_number"]
            Employer_identification = W_Nine_Form.cleaned_data["Employer_identification_number"]
            Certification = W_Nine_Form.cleaned_data["Certification"]
            Signature = W_Nine_Form.cleaned_data["Signature"]
            IP_Address , is_routable  = get_client_ip(request)
            if IP_Address is None:
                IP = "0.0.0.0"
            else:
                if is_routable:
                    IPv = "Public"
                    IP = IP_Address
                else:
                    IPv = "Private"
                    Ip = IP_Address
            print(Ip,IPv)
            if Certification == True:
                Certified = Certification
                object = Usa_Tax_Payer(Name = User_Name, Business_Name = Business, Federal_tax_classification = Federal_tax,Exempt_payee_code = Exempt_payee,Exempt_FATCA_code = Exempt_FATCA, Address = Address, City = City, State = State,Zip_Code = Zip, Social_security_number = Social_security, Employer_identification_number = Employer_identification,Certification = Certified, Signature = Signature,IP = Ip,User = request.user.id)
                object.save()
                return redirect("/pdfloader")
        else:
            W_Nine_Form = USA_W_Nine_Form()
            user_id = request.user.id
            User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
            return render(request,"W9form.html",{"W9_Form":W_Nine_Form,"Profile_Name":User_Name})
    else:
        W_Nine_Form = USA_W_Nine_Form()
        user_id = request.user.id
        User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
    return render(request,"W9form.html",{"W9_Form":W_Nine_Form,"Profile_Name":User_Name})



def Dashboard(request,name):
    if request.session.has_key('uid'):
        Uid = request.session['uid']
        print(Uid)
        try:
            user_id = request.user.id
            User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
            Product_Id_List = Get_Project_Id(Id= user_id)
            if name == User_Name:
                Profile_Image = Influencer_Details.objects.all().filter(User = user_id).values("Profile_Picture")[0]["Profile_Picture"]
                User_Country = Influencer_Details.objects.all().filter(User = user_id).values("Country")[0]["Country"]
                User_Join_Date = Account.objects.all().filter(id = user_id).values("date_joined")[0]["date_joined"]
                Profile_Url = "../../media/{}".format(Profile_Image)
                return render(request, 'dashboard.html',{"Profile_Name":User_Name,"Profile_infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Product_List":Product_Id_List})
        except:
            return HttpResponseBadRequest()
    else:
        return redirect("/Logout")


def Profile(request, name):
    if request.session.has_key('uid'):
        
        try:
            user_id = request.user.id
            Profile_Image = Influencer_Details.objects.all().filter(User = user_id).values("Profile_Picture")[0]["Profile_Picture"]
            User_Country = Influencer_Details.objects.all().filter(User = user_id).values("Country")[0]["Country"]
            User_Details = Influencer_Details.objects.all().filter(User = user_id).values("Descriptions")[0]["Descriptions"]
            User_Phone_Verified = Influencer_Details.objects.all().filter(User = user_id).values("Is_Phone_Verified")[0]["Is_Phone_Verified"]
            User_Email_Verified = Account.objects.all().filter(id = user_id).values("is_email_varified")[0]["is_email_varified"]
            User_Join_Date = Account.objects.all().filter(id = user_id).values("date_joined")[0]["date_joined"]
            Insta_Link = Influencer_Details.objects.all().filter(User = user_id).values("Instagram_Link")[0]["Instagram_Link"]
            YouTube_Link = Influencer_Details.objects.all().filter(User = user_id).values("Youtube_Link")[0]["Youtube_Link"]
            Profile_Url = "../../media/{}".format(Profile_Image)
            try:
                Insta_url = Insta_Link.split('/')[3]
            except:
                Insta_url = "N/A"
            try:
                YouTube_url = YouTube_Link.split('/')[4]
            except:
                YouTube_url = "N/A"

            try:
                id = request.user.id
                Gig_id_Obj = Initial_Data.objects.all().filter(User = id).values("Title","Category_Service","Descriptions","id")
                Gig_Obj ={}
                for i in range(len(Gig_id_Obj)):
                    Urls = Gig_Attachments.objects.all().filter(Gig_Id = int(Gig_id_Obj[i]["id"])).values("Attachments")[i]["Attachments"]
                    Attachment_Url = "../../media/{}".format(Urls)
                    Gig_Obj["Title"] = Gig_id_Obj[i]["Title"]
                    Gig_Obj["Category_Service"] = Gig_id_Obj[i]["Category_Service"]
                    Gig_Obj["Descriptions"] = Gig_id_Obj[i]["Descriptions"]
                    Gig_Obj["Image"] = Attachment_Url
            except:
                Gig_Obj = None
            try:
                Insta_Exist = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("followers")[0]["followers"]
                if Insta_Exist is not None:
                    Insta_Present = True
                else:
                    Insta_Present = False
            except:
                Insta_Present = False
        
            try:
                Youtube_Exist = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Subscribers")[0]["Subscribers"]
                if Youtube_Exist is not None:
                    Youtube_Present = True
                else:
                    Youtube_Present = False
            except:
                Youtube_Present = False
            
            if Insta_url != "N/A" and YouTube_url != "N/A":
                if Insta_Present == True and Youtube_Present == True:
                
                    Followers_Insta = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("followers")[0]["followers"]
                    Verification = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Verified")[0]["Verified"]
                    No_Post = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    YouTube_Subs = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Subscribers")[0]["Subscribers"]
                    Number_of_Posts = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    Views_Last = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Views")[0]["Views"]
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
                elif Insta_Present == True and Youtube_Present == False:
                    Followers_Insta = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("followers")[0]["followers"]
                    Verification = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Verified")[0]["Verified"]
                    No_Post = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    YouTube_Subs = "N/A"
                    Number_of_Posts = "N/A"
                    Views_Last = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
                elif Insta_Present == False and Youtube_Present == True:
                    YouTube_Subs = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Subscribers")[0]["Subscribers"]
                    Number_of_Posts = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    Views_Last = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Views")[0]["Views"]
                    Followers_Insta = "N/A"
                    Verification = "N/A"
                    No_Post = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
                else:
                    Followers_Insta = "N/A"
                    Verification = "N/A"
                    No_Post = "N/A"
                    YouTube_Subs = "N/A"
                    Number_of_Posts = "N/A"
                    Views_Last = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
            elif YouTube_url != "N/A" and Insta_url == "N/A":
                try:
                    YouTube_Subs = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Subscribers")[0]["Subscribers"]
                    Number_of_Posts = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    Views_Last = Youtube_Account_Details.objects.all().filter(Youtube_Link = YouTube_url).values("Views")[0]["Views"]
                    Followers_Insta = "N/A"
                    Verification = "N/A"
                    No_Post = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
                except:
                    YouTube_Subs = "N/A"
                    Number_of_Posts = "N/A"
                    Views_Last = "N/A"
                    Followers_Insta = "N/A"
                    Verification = "N/A"
                    No_Post = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
            elif YouTube_url == "N/A" and Insta_url != "N/A":
                try:
                    Followers_Insta = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("followers")[0]["followers"]
                    Verification = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Verified")[0]["Verified"]
                    No_Post = Instagram_Account_Details.objects.all().filter(Insta_Link =Insta_url).values("Number_of_Posts")[0]["Number_of_Posts"]
                    YouTube_Subs = "N/A"
                    Number_of_Posts = "N/A"
                    Views_Last = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
                except:
                    YouTube_Subs = "N/A"
                    Number_of_Posts = "N/A"
                    Views_Last = "N/A"
                    Followers_Insta = "N/A"
                    Verification = "N/A"
                    No_Post = "N/A"
                    return render(request,'profile.html',{"Profile_Name":name,"Profile_Infos":Profile_Url,"Country":User_Country,"Join_Date":User_Join_Date,"Details":User_Details,"Email_Verified":User_Email_Verified, "Phone_Verified":User_Phone_Verified,"Url_Insta":Insta_url,"Url_Tube":YouTube_url,"Followers_Insta":Followers_Insta,"YouTube_Subs":YouTube_Subs,"Verification":Verification,"No_Post":No_Post,"Number_of_Posts":Number_of_Posts,"Views_Last":Views_Last,"Context_Gigs":Gig_Obj})
        
        except:
            return HttpResponseBadRequest()
    else:
        return redirect("/Logout")
        


def Updater_Insta(request,Insta_Url):
    user_id = request.user.id
    User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
    try:
        Data = Insta_Bot(url=Insta_Url)
        if Data is not None:
            print(Data)
            object = Instagram_Account_Details(Verified = Data["Is_Varified"],Profile_Description =Data["Profile_Description"],Number_of_Posts=Data["Number_of_Posts"],followers =Data["followers"],Insta_Link=Insta_Url)
            object.save()
            return render(request,"Success.html",{"Profile_Name":User_Name})
        else:
            return render(request,"Failed.html",{"Profile_Name":User_Name})
    except:
        return render(request,"Failed.html",{"Profile_Name":User_Name})


def Updater_Youtube(request,url):
    user_id = request.user.id
    User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
    try:
        Data = Youtube_bot(urls= url)
        if Data is not None:
            print(Data)
            object = Youtube_Account_Details(Subscribers = Data["Sub"],Link =Data["Links"],Number_of_Posts=Data["#of_Post"],Views =Data["Views"],Youtube_Link=url)
            object.save()
            return render(request,"Success.html",{"Profile_Name":User_Name})
        else:
            return render(request,"Failed.html",{"Profile_Name":User_Name})
    except:
        return render(request,"Failed.html",{"Profile_Name":User_Name})


def pdfloader(request):
    User_Id = request.user.id
    try:
        Name = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Name")[0]["Name"]
        Business = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Business_Name")[0]["Business_Name"]
        Federal_tax = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Federal_tax_classification")[0]["Federal_tax_classification"]
        Exempt_payee = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Exempt_payee_code")[0]["Exempt_payee_code"]
        Exempt_FATCA = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Exempt_FATCA_code")[0]["Exempt_FATCA_code"]
        Address = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Address")[0]["Address"]
        City = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("City")[0]["City"]
        State = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("State")[0]["State"]
        Zip = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Zip_Code")[0]["Zip_Code"]
        Social_security = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Social_security_number")[0]["Social_security_number"]
        Employer_identification = Usa_Tax_Payer.objects.all().filter(User = User_Id).values("Employer_identification_number")[0]["Employer_identification_number"]

        template_path = 'pdf_downloader.html'
        context = {'Name': Name,
                    "Business_Name":Business,
                    "Typ_Classification":Federal_tax,
                    "Exemption_Payee":Exempt_payee,
                    "Exemption_FATCA":Exempt_FATCA,
                    "Address":Address,
                    "City":City,
                    "State":State,
                    "Zip":Zip,
                    "SSN":Social_security,
                    "EIN":Employer_identification
                    }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        #Object = Pdf_Files(Pdf_File = pisa_status,User = User_Id)
        #Object.save()
        return response
    except:
        return HttpResponseBadRequest()

    
def CreateGigInitial(request):
    if request.session.has_key('uid'):
        user_id = request.user.id
        try:
            Is_Filled=Initial_Data.objects.filter(User = user_id).values("Is_Next_Form_Filled").last()["Is_Next_Form_Filled"]
            if Is_Filled == False:
                Initial_Data.objects.filter(User= user_id).last().delete()
        except:
            pass
        if request.method == "POST":
            Initial_Form = Create_Gig_Form_Initial(request.POST)
            if Initial_Form.is_valid():
                Title_Name = Initial_Form.cleaned_data["Title"]
                Description = Initial_Form.cleaned_data["Descriptions"]
                Category = Initial_Form.cleaned_data["Category_Service"]
                Tags = Initial_Form.cleaned_data["Search_Tags"]
                Initial_Form_Obj = Initial_Data(User = request.user.id,Title = Title_Name, Descriptions = Description, Category_Service  = Category, Search_Tags = Tags, Is_Next_Form_Filled = False)
                Initial_Form_Obj.save()
                return redirect("/PackageForm")
        else:
            Initial_Form = Create_Gig_Form_Initial()
            return render(request, 'Initialform.html',{"Initital_Form":Initial_Form})
    else:
        return redirect("/Logout")
    

def PackageForm(request):
    if request.session.has_key('uid'):
        user_id= request.user.id
        try:
           Is_Filled=Pkg_Form_Data.objects.filter(User = user_id).values("Is_Next_Form_Filled").last()["Is_Next_Form_Filled"]
           if Is_Filled == False:
               Pkg_Form_Data.objects.filter(User= user_id).last().delete()
        except:
            pass
        if request.method == "POST":
            Pkg_Form = Create_Gig_Form_Pkg(request.POST)
            if Pkg_Form.is_valid():
                Besic_PackageName = Pkg_Form.cleaned_data["Besic_Packages_Name"]
                Besic_PackageDescription = Pkg_Form.cleaned_data["Besic_Packages_Descriptions"]
                Besic_PackagePrice = Pkg_Form.cleaned_data["Besic_Packages_Price"]
                Besic_DeliveryTime = Pkg_Form.cleaned_data["Besic_Delivery_Time"]
                
                Standered_PackageName = Pkg_Form.cleaned_data['Standered_Packeges_Name']
                Standered_PackageDes = Pkg_Form.cleaned_data['Standered_Packeges_Description']
                Standered_PackageDel_Time = Pkg_Form.cleaned_data['Standered_Delivery_Time']
                Standered_PackagePrice = Pkg_Form.cleaned_data['Standered_Packeges_Price']
                
                Premium_PackageName = Pkg_Form.cleaned_data['Premium_Packages_Name']
                Premium_PackageDes = Pkg_Form.cleaned_data['Premium_Packages_Descriptions']
                Premium_PackageDel_Time = Pkg_Form.cleaned_data['Premium_Delivery_Time']
                Premium_PackagePrice = Pkg_Form.cleaned_data['Premium_Packages_Price']
                
                Besic_Instagram_Image_to_Feed = Pkg_Form.cleaned_data["Instagram_Image_to_Feed_Besic"]
                Besic_Instagram_Video_to_Feed = Pkg_Form.cleaned_data["Instagram_Video_to_Feed_Besic"]
                Besic_Instagram_Post_to_Story = Pkg_Form.cleaned_data["Instagram_Post_to_Story_Besic"]
                Besic_Instagram_Post_to_Reel = Pkg_Form.cleaned_data["Instagram_Post_to_Reel_Besic"]
                Besic_Instagram_Live_Product_Endorsment = Pkg_Form.cleaned_data["Instagram_Live_Product_Endorsment_Besic"]
                
                Standered_Instagram_Image_to_Feed = Pkg_Form.cleaned_data["Instagram_Image_to_Feed_Std"]
                Standered_Instagram_Video_to_Feed = Pkg_Form.cleaned_data["Instagram_Video_to_Feed_Std"]
                Standered_Instagram_Post_to_Story = Pkg_Form.cleaned_data["Instagram_Post_to_Story_Std"]
                Standered_Instagram_Post_to_Reel = Pkg_Form.cleaned_data["Instagram_Post_to_Reel_Std"]
                Standered_Instagram_Live_Product_Endorsment = Pkg_Form.cleaned_data["Instagram_Live_Product_Endorsment_Std"]
                
                Premium_Instagram_Image_to_Feed= Pkg_Form.cleaned_data["Instagram_Image_to_Feed_Prm"]
                Premium_Instagram_Video_to_Feed = Pkg_Form.cleaned_data["Instagram_Video_to_Feed_Prm"]
                Premium_Instagram_Post_to_Story = Pkg_Form.cleaned_data["Instagram_Post_to_Story_Prm"]
                Premium_Instagram_Post_to_Reel = Pkg_Form.cleaned_data["Instagram_Post_to_Reel_Prm"]
                Premium_Instagram_Live_Product_Endorsment = Pkg_Form.cleaned_data["Instagram_Live_Product_Endorsment_Prm"]
                
                
                Besic_TikTok_Post_to_Feed = Pkg_Form.cleaned_data["TikTok_Post_to_Feed_Besic"]
                Besic_TikTok_Post_Product_Review_Video = Pkg_Form.cleaned_data["TikTok_Post_Product_Review_Video_Besic"]
                Besic_TikTok_Product_Review_Short_Video = Pkg_Form.cleaned_data["TikTok_Product_Review_Short_Video_Besic"]
                Besic_TikTok_Live_Product_Review = Pkg_Form.cleaned_data["TikTok_Live_Product_Review_Besic"]
                
                Standered_TikTok_Post_to_Feed = Pkg_Form.cleaned_data["TikTok_Post_to_Feed_Std"]
                Standered_TikTok_Post_Product_Review_Video = Pkg_Form.cleaned_data["TikTok_Post_Product_Review_Video_Std"]
                Standered_TikTok_Product_Review_Short_Video = Pkg_Form.cleaned_data["TikTok_Product_Review_Short_Video_Std"]
                Standered_TikTok_Live_Product_Review = Pkg_Form.cleaned_data["TikTok_Live_Product_Review_Std"]
                
                Premium_TikTok_Post_to_Feed = Pkg_Form.cleaned_data["TikTok_Post_to_Feed_Prm"]
                Premium_TikTok_Post_Product_Review_Video = Pkg_Form.cleaned_data["TikTok_Post_Product_Review_Video_Prm"]
                Premium_TikTok_Product_Review_Short_Video = Pkg_Form.cleaned_data["TikTok_Product_Review_Short_Video_Prm"]
                Premium_TikTok_Live_Product_Review = Pkg_Form.cleaned_data["TikTok_Live_Product_Review_Prm"]
                
                
                Besic_Duration_Post = Pkg_Form.cleaned_data["Duration_Post_Besic"]
                Besic_Post_Select = Pkg_Form.cleaned_data["Post_Select_Besic"]
                Besic_Duration_Video = Pkg_Form.cleaned_data["Duration_Video_Besic"]
                Besic_Video_Select = Pkg_Form.cleaned_data["Video_Select_Besic"]
                
                Standered_Duration_Post = Pkg_Form.cleaned_data["Duration_Post_Standared"]
                Standered_Post_Select = Pkg_Form.cleaned_data["Post_Select_Standared"]
                Standered_Duration_Video = Pkg_Form.cleaned_data["Duration_Video_Standared"]
                Standered_Video_Select = Pkg_Form.cleaned_data["Video_Select_Standared"]
                
                Premium_Duration_Post = Pkg_Form.cleaned_data["Duration_Post_Premium"]
                Premium_Post_Select = Pkg_Form.cleaned_data["Post_Select_Premium"]
                Premium_Duration_Video = Pkg_Form.cleaned_data["Duration_Video_Premium"]
                Premium_Video_Select = Pkg_Form.cleaned_data["Video_Select_Premium"]
                
                Gig_Ids = Initial_Data.objects.filter(User = user_id).values("id").last()["id"]
                object_to_Save = Pkg_Form_Data(User = user_id,Besic_Packages_Name = Besic_PackageName,Besic_Packages_Descriptions = Besic_PackageDescription,
                                               Besic_Packages_Price = Besic_PackagePrice ,Besic_Delivery_Time =Besic_DeliveryTime,
                                               Standered_Packeges_Name = Standered_PackageName,Standered_Packeges_Description = Standered_PackageDes,
                                               Standered_Delivery_Time = Standered_PackageDel_Time,Standered_Packeges_Price = Standered_PackagePrice,
                                               Premium_Packages_Name = Premium_PackageName,Premium_Packages_Descriptions = Premium_PackageDes, 
                                               Premium_Delivery_Time = Premium_PackageDel_Time, Premium_Packages_Price = Premium_PackagePrice, 
                                               Instagram_Image_to_Feed_Besic = Besic_Instagram_Image_to_Feed,Instagram_Video_to_Feed_Besic = Besic_Instagram_Video_to_Feed,
                                               Instagram_Post_to_Story_Besic = Besic_Instagram_Post_to_Story,Instagram_Post_to_Reel_Besic = Besic_Instagram_Post_to_Reel,
                                               Instagram_Live_Product_Endorsment_Besic = Besic_Instagram_Live_Product_Endorsment,
                                               TikTok_Post_to_Feed_Besic = Besic_TikTok_Post_to_Feed,TikTok_Post_Product_Review_Video_Besic = Besic_TikTok_Post_Product_Review_Video,
                                               TikTok_Product_Review_Short_Video_Besic = Besic_TikTok_Product_Review_Short_Video,TikTok_Live_Product_Review_Besic = Besic_TikTok_Live_Product_Review,
                                               Instagram_Image_to_Feed_Std = Standered_Instagram_Image_to_Feed,Instagram_Video_to_Feed_Std = Standered_Instagram_Video_to_Feed,
                                               Instagram_Post_to_Story_Std = Standered_Instagram_Post_to_Story,Instagram_Post_to_Reel_Std = Standered_Instagram_Post_to_Reel,
                                               Instagram_Live_Product_Endorsment_Std = Standered_Instagram_Live_Product_Endorsment,
                                               TikTok_Post_to_Feed_Std = Standered_TikTok_Post_to_Feed,TikTok_Post_Product_Review_Video_Std =Standered_TikTok_Post_Product_Review_Video,
                                               TikTok_Product_Review_Short_Video_Std = Standered_TikTok_Product_Review_Short_Video,TikTok_Live_Product_Review_Std = Standered_TikTok_Live_Product_Review,
                                               Instagram_Image_to_Feed_Prm = Premium_Instagram_Image_to_Feed,Instagram_Video_to_Feed_Prm = Premium_Instagram_Video_to_Feed,
                                               Instagram_Post_to_Story_Prm = Premium_Instagram_Post_to_Story,Instagram_Post_to_Reel_Prm = Premium_Instagram_Post_to_Reel,
                                               Instagram_Live_Product_Endorsment_Prm = Premium_Instagram_Live_Product_Endorsment,
                                               TikTok_Post_to_Feed_Prm = Premium_TikTok_Post_to_Feed,TikTok_Post_Product_Review_Video_Prm = Premium_TikTok_Post_Product_Review_Video,
                                               TikTok_Product_Review_Short_Video_Prm = Premium_TikTok_Product_Review_Short_Video,TikTok_Live_Product_Review_Prm = Premium_TikTok_Live_Product_Review,
                                               Duration_Post_Besic = Besic_Duration_Post,Post_Select_Besic = Besic_Post_Select, Duration_Video_Besic = Besic_Duration_Video,
                                               Video_Select_Besic = Besic_Video_Select,Duration_Post_Standared = Standered_Duration_Post, Post_Select_Standared = Standered_Post_Select,
                                               Duration_Video_Standared = Standered_Duration_Video,Video_Select_Standared = Standered_Video_Select,
                                               Duration_Post_Premium = Premium_Duration_Post, Post_Select_Premium = Premium_Post_Select,
                                               Duration_Video_Premium = Premium_Duration_Video, Video_Select_Premium = Premium_Video_Select, Is_Next_Form_Filled =False,Gig_Id = Gig_Ids)
                object_to_Save.save()
                return redirect("/Describe")
        else:
            Pkg_Form = Create_Gig_Form_Pkg()
            return render(request,'PkgForm.html',{"Initital_Form":Pkg_Form})
    else:
        return redirect("/Logout")



def Describe(request):
    if request.session.has_key('uid'):
        if request.method == "POST":
            Describe_Form = Create_Gig_Form_Describe(request.POST)
            if Describe_Form.is_valid():
                Describe_About = Describe_Form.cleaned_data["Describe_About_Gig"]
                Last_Id = Initial_Data.objects.filter(User = request.user.id).values("id").last()["id"]
                Describe_obj= Describe_Gig(Describe_About_Gig = Describe_About, User = request.user.id,Gig_Id= Last_Id)
                Describe_obj.save()

                User_Recipent = Get_Recipent_User()
                Initial_Data.objects.filter(id = Last_Id).update(Is_Next_Form_Filled = True)
                Last_Id_Pkg = Pkg_Form_Data.objects.filter(User = request.user.id).values("id").last()["id"]
                Pkg_Form_Data.objects.filter(id = Last_Id_Pkg).update(Is_Next_Form_Filled = True)
                notify.send(request.user,recipient= User_Recipent, verb= "{} Created a New Gig, Check it Out")
                Notify_Obj = Notification_Data(Sender_id = request.user.id, Topic = "{} Created a New Gig, Check it Out".format(request.user.username),Type = "Gig_Creation", Gig_Id = Last_Id )
                Notify_Obj.save()
                return redirect("/Gig_Attachment")

        else:
            Describe_Form = Create_Gig_Form_Describe()
            return render(request,'Describeform.html',{"Initital_Form":Describe_Form})
    else:
        return redirect("/Logout")   


def Gig_Attachment(request):
    if request.method == "POST":
        Attachment_Form = Create_Gig_Form_Attachment(request.POST, request.FILES)
        if Attachment_Form.is_valid():
            Thumbnail_Image = request.FILES["Work_Thumbnails"]
            Attachment_Image = request.FILES["Attachments"]
            #Thumbnail_Image_W,Thumbnail_Image_H = get_image_dimensions(Thumbnail_Image)
            #Attachment_Image_W, Attachment_Image_H = get_image_dimensions(Attachment_Image)

            content_type = Thumbnail_Image.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if Thumbnail_Image.size > int(settings.MAX_UPLOAD_THUMB_SIZE) or Attachment_Image.size > int(settings.MAX_UPLOAD_IMAGE_SIZE):
                    raise ValidationError('Please keep Thumb nail filesize under {}. and Attachment Filesize Under {}'.format((filesizeformat(settings.MAX_UPLOAD_THUMB_SIZE), filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
                else:
                    try:
                        id = request.user.id
                        Gig_id_Obj = Initial_Data.objects.filter(User = id).values("id").last()["id"]
                        Attachments_Obj = Gig_Attachments(Work_Thumbnails = Thumbnail_Image, Attachments = Attachment_Image,Gig_Id = Gig_id_Obj )
                        Attachments_Obj.save()
                        User_Name = Influencer_Details.objects.all().filter(User = id).values("Slug_Name")[0]["Slug_Name"]
                        return redirect("/Profile/{}".format(User_Name))
                    except:
                        return HttpResponseBadRequest()
        else:
            Attachment_Form = Create_Gig_Form_Attachment()
            return render(request, "uploadattachment.html",{"Image_Field":Attachment_Form})
    else:
        Attachment_Form = Create_Gig_Form_Attachment()
    return render(request, "uploadattachment.html",{"Image_Field":Attachment_Form})

def Gig(request):
    #try:
    user_id = request.user.id
    User_Name = Influencer_Details.objects.all().filter(User = user_id).values("Slug_Name")[0]["Slug_Name"]
    Gig_id_Obj = Initial_Data.objects.all().values("Title","Category_Service","Descriptions","id")
    Attachment_Url = "../../media/Thunbnail/glass_Full.png"
    Gigs_List = []
    for i in Gig_id_Obj:
        try:
            Urls = Gig_Attachments.objects.all().filter(Gig_Id = i["id"]).values("Attachments")[0]["Attachments"]
        except:
            Urls =None
        if Urls is not None:
            Profile_Url = "../../media/{}".format(Urls)
            i["image"] = Profile_Url
        else:
            i["image"] = Attachment_Url
    return render(request,"Gigs.html",{"Context_Gigs":Gig_id_Obj,"Profile":User_Name})
    #except:
        #return HttpResponseBadRequest()



def Gigdetails(request,title):
    try:
        Gig_Objects = Pkg_Form_Data.objects.all().filter(Gig_Id = int(title)).values("Besic_Packages_Name","Besic_Packages_Price","Besic_Packages_Descriptions","Besic_Delivery_Time","Standered_Packeges_Name",
        "Standered_Packeges_Price","Standered_Packeges_Description","Standered_Delivery_Time","Premium_Packages_Name",
        "Premium_Packages_Price","Premium_Packages_Descriptions","Premium_Delivery_Time","Instagram_Image_to_Feed_Besic","Instagram_Video_to_Feed_Besic",
        "Instagram_Post_to_Story_Besic","Instagram_Post_to_Reel_Besic","Instagram_Live_Product_Endorsment_Besic","TikTok_Post_to_Feed_Besic",
        "TikTok_Post_Product_Review_Video_Besic","TikTok_Product_Review_Short_Video_Besic","TikTok_Live_Product_Review_Besic","Instagram_Image_to_Feed_Std",
        "Instagram_Video_to_Feed_Std","Instagram_Post_to_Story_Std","Instagram_Post_to_Reel_Std","Instagram_Live_Product_Endorsment_Std","TikTok_Post_to_Feed_Std","TikTok_Post_Product_Review_Video_Std",
        "TikTok_Product_Review_Short_Video_Std","TikTok_Live_Product_Review_Std","Instagram_Image_to_Feed_Prm","Instagram_Video_to_Feed_Prm","Instagram_Post_to_Story_Prm",
        "Instagram_Post_to_Reel_Prm","Instagram_Live_Product_Endorsment_Prm","TikTok_Post_to_Feed_Prm","TikTok_Post_Product_Review_Video_Prm","TikTok_Product_Review_Short_Video_Prm","TikTok_Live_Product_Review_Prm"
        ,"id")

        Titles = Initial_Data.objects.all().filter(id = int(title)).values("Title")[0]["Title"]
        print(type(Gig_Objects[0]["Standered_Packeges_Price"]))
        arguemnts_basic = "Basic_{}".format(title)
        arguemnts_standared = "std_{}".format(title)
        arguemnts_prm = "prm_{}".format(title)
        return render(request,'Gig-details.html',{"Context_items":Gig_Objects,"bs":arguemnts_basic,"sd":arguemnts_standared, "pm":arguemnts_prm,"Title":Titles})
    except:
        return HttpResponseBadRequest()
#def Update_Start():
    #Scheduler= BackgroundScheduler()
    #Scheduler.add_job(Insta_Data_Save,'interval', minutes=5)
    #Scheduler.start()
