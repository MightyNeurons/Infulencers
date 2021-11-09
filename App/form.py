from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.db.models import fields
from django.forms import Form
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Account, Acount_Influencer, Influencer_Details, Usa_Tax_Payer, Gigs
from .backends import AccountAuth


class Register_Forms(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(),validators=[validate_password])
	class Meta:
		model = Account
		fields = ("email", "username", "password")
		label = {

			"email": "Email",
			"username": "Username",
			"password": "Password",

		}



class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    password =  forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)

class Is_Influencer_Form(ModelForm):
	class Meta:
		model = Acount_Influencer
		fields = ("Is_Influencer","Is_Hiring_Influencer")
		label = {

			"Is_Influencer": "I'll Work",
			"Is_Hiring_Influencer": "I'll Hire",

		}
		



class Details_Inf(ModelForm):
	Tiktok_Link = forms.CharField(max_length=500, required=False,widget=forms.TextInput(attrs={"class":"Tiktok_Class", "id":"TikTok", "placeholder":"TikTok Profile Link"}))
	Instagram_Link = forms.CharField(max_length=500, required=False,widget=forms.TextInput(attrs={"class":"Insta_Class", "id":"Insta", "placeholder":"Instagram Profile Link"}))
	Youtube_Link = forms.CharField(max_length=500, required=False,widget=forms.TextInput(attrs={"class":"YouTube_Class", "id":"YouTube", "placeholder":"Youtube Profile Link"}))

	class Meta:
		model = Influencer_Details
		fields = ("First_Name","Last_Name","Profile_Picture","Descriptions","Audience","Country","Tiktok_Link","Instagram_Link","Youtube_Link","Phone_Number")
		label = {

			"First_Name": "First Name",
			"Last_Name": "Last Name",
			"Profile_Picture" : "Profile Picture",
			"Descriptions":"Tell us more about you",
			"Audience":"Audience",
			"Country":"Country",
			"Tiktok_Link":"Tiktok Link",
			"Instagram_Link":"Instagram Link",
			"Youtube_Link":"Youtube Link",
			"Phone_Number":"Phone Number",
		}


class OTP_form(forms.Form):
	Otp = forms.IntegerField(label="Enter OTP to Verify")



Tax_Clssification_Options = (
	("Individual/sole proprietor or single-member LLC", "Individual/sole proprietor or single-member LLC"),
	("C Corporation", "C Corporation"),
	("S Corporation", "S Corporation"),
	("Partnership", "Trust/estate"),
	("Limited liability company.(corporation)", "Limited liability company.(corporation)"),
	("Limited liability company.(corporation)", "Limited liability company.(corporation)"),
	("Limited liability company.(Partnership)", "Limited liability company.(Partnership)"),
	("Other", "Other "),
)

class USA_W_Nine_Form(ModelForm):
	Federal_tax_classification = forms.ChoiceField(choices=Tax_Clssification_Options, required=True)
	Exempt_payee_code = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class":"Payee", "id":"Payee_Id", "placeholder":"Enter Your Exempt payee code (if any)"}))
	Exempt_FATCA_code = forms.CharField(required=False,widget=forms.TextInput(attrs={"class":"FATCA", "id":"FATCA_Id","placeholder":"Enter Your Exempt FATCA code (if any)"}))
	Social_security_number = forms.IntegerField(required=False, widget= forms.NumberInput(attrs={"class":"Ss_Number", "id":"Ss_Number_Id","placeholder":"Enter Your Social security number"}))
	Employer_identification_number = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class":"EIN", "id":"EIN_Id","placeholder":"Enter Your Employer identification number"}))
	Signature = forms.CharField(required=False,widget=forms.TextInput(attrs={"class":"Sign", "id":"Sign_Id","placeholder":"By Entering Your Name Here You agreeing that our terms and conditions"}))
	class Meta:
		model = Usa_Tax_Payer
		fields = ("Name","Business_Name","Federal_tax_classification","Exempt_payee_code","Exempt_FATCA_code","Address","City","State","Zip_Code","Social_security_number","Employer_identification_number","Certification","Signature")
		label = {
			"Name":"Name",
			"Business_Name": "Business Name",
			"Federal_tax_classification" : "Select any Federal tax classification of the person whose name is entered",
			"Exempt_payee_code" : "Exempt payee code",
			"Exempt_FATCA_code" : "Exempt FATCA code",
			"Address" : "Address",
			"City": "City",
			"State":"State" ,
			"Zip_Code": "Zip Code",
			"Social_security_number": "Social security number",
			"Employer_identification_number":"Employer identification number",
			"Certification": "Please Check the box before submitting",
			"Signature":"Signature",
		}



class Gig_Search(forms.Form):
    search = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={"class":"Form_Class", "id":"tags", "placeholder":"Search Products Here"}))



Skills = (
	("Instagram Post","Instagram Post"),
	("TikTok - Post","TikTok - Post"),
)


Post = (
	("Hours","Hours"),
	("Days","Days"),
	("Week","Week"),
)

Video = (
	("Sec","Sec"),
	("Min","Min"),
	("Hr","Hr"),
)

class Create_Gig_Form_Initial(forms.Form):
	Title = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id"}),label="Create Your Gig Title")
	Descriptions = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_2"}),label="Describe Your Gig", min_length=50, max_length=100)
	Category_Service = forms.ChoiceField(choices=Skills, label="Choose Your Category")
	Search_Tags = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_3"}),label="Create Search Tags")
	

class Create_Gig_Form_Pkg(forms.Form):
	Besic_Packages_Name = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id"}), label="Basic Package Name")
	Standered_Packeges_Name = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_2"}), label="Standared Package Name")
	Premium_Packages_Name = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_3"}), label="Premium Package Name")

	Besic_Packages_Descriptions = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_4"}),label="Basic Package Descriptions",min_length=50, max_length=100)
	Standered_Packeges_Description =forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_5"}),label="Standared Package Descriptions",min_length=50, max_length=100)
	Premium_Packages_Descriptions = forms.CharField(widget=forms.TextInput(attrs={"class":"input--style-1","id":"Input_id_6"}),label="Premium Package Descriptions",min_length=50, max_length=100)

	Besic_Delivery_Time = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_7"}),label="Bascis Package Delivery Time(in Days)", min_value=1)
	Premium_Delivery_Time = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_8"}),label="Premium Package Delivery Time(in Days)", min_value=1)
	Standered_Delivery_Time = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_9"}),label="Standared Package Delivery Time(in Days)", min_value=1)

	Besic_Packages_Price = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_10"}),label="Basic Package Starting Price", min_value=1)
	Standered_Packeges_Price = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_11"}),label="Standared Package Starting Price", min_value=1)
	Premium_Packages_Price = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_12"}),label="Premium Package Starting Price", min_value=1)
	

	Instagram_Image_to_Feed_Besic = forms.BooleanField(label="Insta Image to Feed",required=False)
	Instagram_Video_to_Feed_Besic = forms.BooleanField(label="Insta Video to Feed Besic",required=False)
	Instagram_Post_to_Story_Besic = forms.BooleanField(label="Insta Post to Story",required=False)
	Instagram_Post_to_Reel_Besic = forms.BooleanField(label="Insta Post to Reel",required=False)
	Instagram_Live_Product_Endorsment_Besic = forms.BooleanField(label="Insta Live Product Endorsment",required=False)
	TikTok_Post_to_Feed_Besic = forms.BooleanField(label="TikTok Post to Feed",required=False)
	TikTok_Post_Product_Review_Video_Besic = forms.BooleanField(label="Tiktok Post Product Review Video",required=False)
	TikTok_Product_Review_Short_Video_Besic = forms.BooleanField(label="TikTok Product Review Short Video",required=False)
	TikTok_Live_Product_Review_Besic = forms.BooleanField(label="TikTok Live Product Review",required=False)

	Instagram_Image_to_Feed_Std = forms.BooleanField(label="Insta Image to Feed",required=False)
	Instagram_Video_to_Feed_Std = forms.BooleanField(label="Insta Video to Feed Besic",required=False)
	Instagram_Post_to_Story_Std = forms.BooleanField(label="Insta Post to Story",required=False)
	Instagram_Post_to_Reel_Std = forms.BooleanField(label="Insta Post to Reel",required=False)
	Instagram_Live_Product_Endorsment_Std = forms.BooleanField(label="Insta Live Product Endorsment",required=False)
	TikTok_Post_to_Feed_Std = forms.BooleanField(label="TikTok Post to Feed",required=False)
	TikTok_Post_Product_Review_Video_Std = forms.BooleanField(label="Tiktok Post Product Review Video",required=False)
	TikTok_Product_Review_Short_Video_Std = forms.BooleanField(label="TikTok Product Review Short Video",required=False)
	TikTok_Live_Product_Review_Std = forms.BooleanField(label="TikTok Live Product Review",required=False)

	Instagram_Image_to_Feed_Prm = forms.BooleanField(label="Insta Image to Feed",required=False)
	Instagram_Video_to_Feed_Prm = forms.BooleanField(label="Insta Video to Feed Besic",required=False)
	Instagram_Post_to_Story_Prm = forms.BooleanField(label="Insta Post to Story",required=False)
	Instagram_Post_to_Reel_Prm = forms.BooleanField(label="Insta Post to Reel",required=False)
	Instagram_Live_Product_Endorsment_Prm = forms.BooleanField(label="Insta Live Product Endorsment",required=False)
	TikTok_Post_to_Feed_Prm = forms.BooleanField(label="TikTok Post to Feed",required=False)
	TikTok_Post_Product_Review_Video_Prm = forms.BooleanField(label="Tiktok Post Product Review Video",required=False)
	TikTok_Product_Review_Short_Video_Prm = forms.BooleanField(label="TikTok Product Review Short Video",required=False)
	TikTok_Live_Product_Review_Prm = forms.BooleanField(label="TikTok Live Product Review",required=False)


	Duration_Post_Besic = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_13"}),label="Post Duration", min_value=1,max_value=60,required=False)
	Post_Select_Besic = forms.ChoiceField(choices=Post,required=False)
	Duration_Video_Besic = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_14"}),label="Video Duration",min_value=1,max_value=3660,required=False)
	Video_Select_Besic = forms.ChoiceField(choices=Video,required=False)

	Duration_Post_Standared = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_15"}),label="Post Duration", min_value=1,max_value=60,required=False)
	Post_Select_Standared = forms.ChoiceField(choices=Post,required=False)
	Duration_Video_Standared = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_16"}),label="Video Duration",min_value=1,max_value=3660,required=False)
	Video_Select_Standared = forms.ChoiceField(choices=Video,required=False)

	Duration_Post_Premium = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_17"}),label="Post Duration", min_value=1,max_value=60,required=False)
	Post_Select_Premium = forms.ChoiceField(choices=Post,required=False)
	Duration_Video_Premium = forms.IntegerField( widget=forms.NumberInput(attrs={"class":"input--style-1","id":"Input_id_18"}),label="Video Duration",min_value=1,max_value=3660,required=False)
	Video_Select_Premium = forms.ChoiceField(choices=Video,required=False)
	
class Create_Gig_Form_Describe(forms.Form):
	Describe_About_Gig = forms.CharField(min_length=100, max_length=500)

class Create_Gig_Form_Attachment(forms.Form):
	
	Work_Thumbnails = forms.ImageField(label="Upload Thumbnail", widget=forms.FileInput(attrs={"class":"input-file", "id": "my-file"}))
	Attachments = forms.ImageField(label="Upload Your Image/Video", widget=forms.FileInput(attrs={"class":"input-file", "id": "my-file"}))


