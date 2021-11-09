import uuid
from django.db import models
from django import forms
from django.db import models
from django.db.models.base import Model
from django.forms import forms
from django.db.models.fields import CharField, EmailField
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
import datetime
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    is_email_varified		= models.BooleanField(default=False)
    UUid_Token		= models.UUIDField(default=str(uuid.uuid4()), editable=False)
	

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class Acount_Influencer(models.Model):
	User = models.IntegerField(primary_key=True)
	Is_Influencer = models.BooleanField(default=False)
	Is_Hiring_Influencer = models.BooleanField(default=False)

Audience_CHOICES = (
	("Select", "Select"),
    ("6 and Under", "6 and Under"),
    ("7 to 12", "7 to 12"),
    ("13 to 17", "13 to 17"),
    ("18 to 30", "18 to 30"),
    ("31 to 40", "31 to 40"),
    ("41 to 50", "41 to 50"),
    ("50 and older", "50 and older"),
)

Country_CHOICES = (
	("Select", "Select"),
    ("Afghanistan", "Afghanistan"),
    ("Armenia", "Armenia"),
    ("Azerbaijan", "Azerbaijan"),
	("Albania", "Albania"),
	("Andorra", "Andorra"),
	("Austria", "Austria"),
	("Argentina", "Argentina"),
    ("Bahrain", "Bahrain"),
    ("Bangladesh", "Bangladesh"),
    ("Bhutan", "Bhutan"),
    ("Brunei", "Brunei"),
	("Burma", "Burma"),
	("Belarus", "Belarus"),
	("Belgium", "Belgium"),
	("Bulgaria", "Bulgaria"),
	("Bosnia and Herzegovina", "Bosnia and Herzegovina"),
	("Brazil", "Brazil"),
	("Croatia", "Croatia"),
	("Czech Republic", "Czech Republic"),
	("Cambodia", "Cambodia"),
	("Colombia", "Colombia"),
	("China", "China"),
	("Cameroon", "Cameroon"),
	("Cyprus", "Cyprus"),
	("Central African Republic", "Central African Republic"),
	("Canada", "Canada"),
	("Chile", "Chile"),
	("Democratic Republic of the Congo", "Democratic Republic of the Congo"),
	("Denmark", "Denmark"),
	("Egypt", "Egypt"),
	("Ethiopia", "Ethiopia"),
	("Finland", "Finland"),
	("France", "France"),
	("Germany", "Germany"),
	("Greece", "Greece"),
	("Ghana", "Ghana"),
	("Georgia", "Georgia"),
	("Hungary", "Hungary"),
	("India", "India"),
	("Iceland", "Iceland"),
	("Ireland", "Ireland"),
	("Italy", "Italy"),
	("Indonesia", "Indonesia"),
	("Iran", "Iran"),
	("Iraq", "Iraq"),
	("Israel", "Israel"),
	("Japan", "Japan"),
	("Jordan", "Jordan"),
	("Kazakhstan", "Kazakhstan"),
	("Kuwait", "Kuwait"),
	("Kyrgyzstan", "Kyrgyzstan"),
	("Kenya", "Kenya"),
	("Laos", "Laos"),
	("Lebanon", "Lebanon"),
	("Malaysia", "Malaysia"),
	("Morocco", "Morocco"),
	("Mexico", "Mexico"),
	("Nepal", "Nepal"),
	("Norway", "Norway"),
	("Netherlands", "Netherlands"),
	("Pakistan", "Pakistan"),
	("Palestine", "Palestine"),
	("Philippines", "Philippines"),
	("Poland", "Poland"),
	("Portugal", "Portugal"),
	("Romania", "Romania"),
	("Russia", "Russia"),
	("Qatar", "Qatar"),
	("Saudi Arabia", "Saudi Arabia"),
	("Singapore", "Singapore"),
	("South Africa", "South Africa"),
	("South Korea", "South Korea"),
	("Sri Lanka", "Sri Lanka"),
	("Spain", "Spain"),
	("Sweden", "Sweden"),
	("Switzerland", "Switzerland"),
	("Thailand", "Thailand"),
	("Turkey", "Turkey"),
	("United Arab Emirates", "United Arab Emirates"),
	("Uganda", "Uganda"),
	("Ukraine", "Ukraine"),
	("United Kingdom", "United Kingdom"),
	("United States", "United States"),
	("Uruguay", "Uruguay"),
	("Zimbabwe", "Zimbabwe"),
	
)


class Influencer_Details(models.Model):
	User = models.IntegerField(primary_key=True)
	Profile_Picture = models.ImageField(upload_to='images/')
	First_Name = models.CharField(max_length=100)
	Last_Name = models.CharField(max_length=150)
	Slug_Name = models.SlugField(max_length=200)
	Descriptions = models.CharField(max_length=800)
	Audience = models.CharField(max_length=20,choices=Audience_CHOICES, default="Select")
	Country = models.CharField(max_length=100,choices=Country_CHOICES, default="Select" )
	Tiktok_Link = models.CharField(max_length=500, null=True)
	Instagram_Link = models.CharField(max_length=500,null=True)
	Youtube_Link = models.CharField(max_length=500,null=True)
	Phone_Number = PhoneNumberField(blank = True)
	Is_Phone_Verified = models.BooleanField(default=False)
	Otp = models.IntegerField(null=True)



class Instagram_Account_Details(models.Model):
	Verified = models.CharField(max_length=50)
	Profile_Description = models.CharField(max_length=800)
	Number_of_Posts = models.CharField(max_length=50)
	followers = models.CharField(max_length=50)
	Insta_Link = models.CharField(max_length=200, default="N/A")
	Scrapping_Time = models.DateTimeField(auto_now_add=True)

class Youtube_Account_Details(models.Model):
	Subscribers = models.CharField(max_length=50)
	Link = models.CharField(max_length=2000)
	Number_of_Posts = models.IntegerField(default=0)
	Views = models.CharField(max_length=800)
	Youtube_Link = models.CharField(max_length=200, default="N/A")
	Scrapping_Time = models.DateTimeField(auto_now_add=True)

class Insta_Scrape(models.Model):
	Raw_Data = models.CharField(max_length=10000)
	DateCreated = models.DateTimeField(auto_now_add=True)

class Usa_Tax_Payer(models.Model):
	Name = models.CharField(max_length=500)
	Business_Name = models.CharField(max_length=1000)
	Federal_tax_classification =  models.CharField(max_length=50)
	Exempt_payee_code = models.IntegerField( default= 000000000, null=True)
	Exempt_FATCA_code = models.CharField(max_length=50, default="N/A", null=True)
	Address = models.CharField(max_length=500)
	City = models.CharField(max_length=50)
	State = models.CharField(max_length=50)
	Zip_Code = models.CharField(max_length=10)
	Social_security_number = models.IntegerField(default= 000000000,null=True)
	Employer_identification_number = models.IntegerField( default= 000000000, null=True)
	Certification = models.BooleanField(default=False)
	Signature = models.CharField(max_length=200)
	Date = models.DateTimeField(auto_now_add=True)
	IP = models.CharField(max_length=10,default="0.0.0.0")
	User = models.IntegerField(primary_key=True)




class Initial_Data(models.Model):
    User = models.IntegerField(default=999999)
    Title = models.CharField(max_length=200)
    Descriptions = models.CharField(max_length=800)
    Category_Service = models.CharField(max_length=100)
    Search_Tags = models.CharField(max_length=200)
    Date_Created = models.DateTimeField(auto_now_add=True)
    Is_Next_Form_Filled = models.BooleanField(default=False)
    


class Pkg_Form_Data(models.Model):
	User = models.IntegerField(default=999999)
	Besic_Packages_Name = models.CharField(max_length=100)
	Besic_Packages_Price = models.IntegerField()
	Besic_Packages_Descriptions = models.CharField(max_length=500)
	Besic_Delivery_Time = models.IntegerField()
	Standered_Packeges_Name = models.CharField(max_length=100)
	Standered_Packeges_Price = models.IntegerField()
	Standered_Packeges_Description = models.CharField(max_length=500)
	Standered_Delivery_Time = models.IntegerField()
	Premium_Packages_Name = models.CharField(max_length=100)
	Premium_Packages_Price = models.IntegerField()
	Premium_Packages_Descriptions = models.CharField(max_length=500)
	Premium_Delivery_Time = models.IntegerField()
	Instagram_Image_to_Feed_Besic = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Besic = models.BooleanField(default=False)
	Instagram_Post_to_Story_Besic = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Besic = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Besic = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Besic = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Besic = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Besic = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Besic = models.BooleanField(default=False)
	Instagram_Image_to_Feed_Std = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Std = models.BooleanField(default=False)
	Instagram_Post_to_Story_Std = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Std = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Std = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Std = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Std = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Std = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Std = models.BooleanField(default=False)
	Instagram_Image_to_Feed_Prm = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Prm = models.BooleanField(default=False)
	Instagram_Post_to_Story_Prm = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Prm = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Prm = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Prm = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Prm = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Prm = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Prm = models.BooleanField(default=False)
	Duration_Post_Besic = models.IntegerField(null=True)
	Post_Select_Besic = models.CharField(max_length=10,null=True)
	Duration_Video_Besic = models.IntegerField(null=True)
	Video_Select_Besic = models.CharField(max_length=10,null=True)
	Duration_Post_Standared = models.IntegerField(null=True)
	Post_Select_Standared = models.CharField(max_length=10,null=True)
	Duration_Video_Standared = models.IntegerField(null=True)
	Video_Select_Standared = models.CharField(max_length=10,null=True)
	Duration_Post_Premium = models.IntegerField(null=True)
	Post_Select_Premium = models.CharField(max_length=10,null=True)
	Duration_Video_Premium = models.IntegerField(null=True)
	Video_Select_Premium = models.CharField(max_length=10,null=True)
	Date_Created = models.DateTimeField(auto_now_add=True)
	Is_Next_Form_Filled = models.BooleanField(default=False)
	Gig_Id = models.IntegerField()
    

class Describe_Gig(models.Model):
	User = models.IntegerField(default=999999)
	Describe_About_Gig = models.CharField(max_length=500,default="N/A")
	Date_Created = models.DateTimeField(auto_now_add=True)
	Gig_Id = models.IntegerField()
    
 
    

class Gigs(models.Model):
	User = models.IntegerField(default=999999)
	Title = models.CharField(max_length=200)
	Descriptions = models.CharField(max_length=800)
	Category_Service = models.CharField(max_length=100)
	Search_Tags = models.CharField(max_length=200)
	Besic_Packages_Name = models.CharField(max_length=100)
	Besic_Packages_Price = models.IntegerField()
	Besic_Packages_Descriptions = models.CharField(max_length=500)
	Besic_Delivery_Time = models.IntegerField()
	Standered_Packeges_Name = models.CharField(max_length=100)
	Standered_Packeges_Price = models.IntegerField()
	Standered_Packeges_Description = models.CharField(max_length=500)
	Standered_Delivery_Time = models.IntegerField()
	Premium_Packages_Name = models.CharField(max_length=100)
	Premium_Packages_Price = models.IntegerField()
	Premium_Packages_Descriptions = models.CharField(max_length=500)
	Premium_Delivery_Time = models.IntegerField()

	Instagram_Image_to_Feed_Besic = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Besic = models.BooleanField(default=False)
	Instagram_Post_to_Story_Besic = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Besic = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Besic = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Besic = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Besic = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Besic = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Besic = models.BooleanField(default=False)
	Instagram_Image_to_Feed_Std = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Std = models.BooleanField(default=False)
	Instagram_Post_to_Story_Std = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Std = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Std = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Std = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Std = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Std = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Std = models.BooleanField(default=False)
	Instagram_Image_to_Feed_Prm = models.BooleanField(default=False)
	Instagram_Video_to_Feed_Prm = models.BooleanField(default=False)
	Instagram_Post_to_Story_Prm = models.BooleanField(default=False)
	Instagram_Post_to_Reel_Prm = models.BooleanField(default=False)
	Instagram_Live_Product_Endorsment_Prm = models.BooleanField(default=False)
	TikTok_Post_to_Feed_Prm = models.BooleanField(default=False)
	TikTok_Post_Product_Review_Video_Prm = models.BooleanField(default=False)
	TikTok_Product_Review_Short_Video_Prm = models.BooleanField(default=False)
	TikTok_Live_Product_Review_Prm = models.BooleanField(default=False)


	Duration_Post_Besic = models.IntegerField(null=True)
	Post_Select_Besic = models.CharField(max_length=10,null=True)
	Duration_Video_Besic = models.IntegerField(null=True)
	Video_Select_Besic = models.CharField(max_length=10,null=True)

	Duration_Post_Standared = models.IntegerField(null=True)
	Post_Select_Standared = models.CharField(max_length=10,null=True)
	Duration_Video_Standared = models.IntegerField(null=True)
	Video_Select_Standared = models.CharField(max_length=10,null=True)

	Duration_Post_Premium = models.IntegerField(null=True)
	Post_Select_Premium = models.CharField(max_length=10,null=True)
	Duration_Video_Premium = models.IntegerField(null=True)
	Video_Select_Premium = models.CharField(max_length=10,null=True)

	Describe_About_Gig = models.CharField(max_length=500,default="N/A")

	Date_Created = models.DateTimeField(auto_now_add=True)


class Gig_Attachments(models.Model):
	Work_Thumbnails = models.ImageField(upload_to='Thunbnail/')
	Attachments = models.ImageField(upload_to='Attachment/')
	Gig_Id = models.IntegerField(primary_key=True)

