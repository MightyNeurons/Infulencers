from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index, name="index"),
    path("About", views.about, name="about"),
    path("Login", views.Login, name="Login"),
    path("Register", views.Registrations, name="Register"),
    path("Logout", views.Logout, name="Logout"),
    path("Is_Influencer",views.Is_Influencer,name="Is_Influencer"),
    path("Mail_Sent",views.Mail_Sent,name="Mail_Sent"),
    path("Verify/<Token>",views.Verify, name="Verify"),
    path("Welcome_Influencer",views.Welcome_Influencer, name="Welcome_Influencer"),
    path("Welcome_Hiring_Manager",views.Welcome_Hiring_Manager, name="Welcome_Hiring_Manager"),
    path("Details_Influencer",views.Details_Influencer, name="Details_Influencer"),
    path("otp",views.otp, name="otp"),
    path("Dashboard/<name>", views.Dashboard,name="Dashboard"),
    path("Profile/<name>", views.Profile,name="Profile"),
    path("Updater/<Insta_Url>", views.Updater_Insta,name="Updater"),
    path("UpdaterYouTube/<url>", views.Updater_Youtube,name="UpdaterYouTube"),
    path("UsaTaxForm", views.UsaTaxForm,name="UsaTaxForm"),
    path("pdfloader", views.pdfloader,name="pdfloader"),
    path("CreateGigInitial", views.CreateGigInitial,name="CreateGigInitial"),
    path("PackageForm", views.PackageForm,name="PackageForm"),
    path("Describe", views.Describe,name="Describe"),
    path("Gig_Attachment", views.Gig_Attachment,name="Gig_Attachment"),
    path("Gig", views.Gig,name="Gig"),
    path("Gigdetails/<title>", views.Gigdetails,name="Gigdetails"),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)