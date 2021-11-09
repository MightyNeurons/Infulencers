from django.http import request
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from App.models import Pkg_Form_Data, Influencer_Details, Account
from .Checkoutform import buyersform
import json
from .models import Checkout_Data, Buyers, Notification_Data, Project_Creation
from notifications.signals import notify

# Create your views here.


def Checkout(request,id):
    Split_Str = str(id).split("_",2)
    try:
        if Split_Str[0] == "Basic":
            Context = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Split_Str[1])).values("Besic_Packages_Price","Besic_Packages_Name","Besic_Packages_Descriptions")
            Package = "Basic"
        elif Split_Str[0]== "std":
            Context = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Split_Str[1])).values("Standered_Packeges_Price","Standered_Packeges_Description","Standered_Packeges_Name")
            #Context[0]["Pkg"] = "Sd"
            Package = "Standared"
        else:
            Context = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Split_Str[1])).values("Premium_Packages_Price","Premium_Packages_Name","Premium_Packages_Descriptions")
            #Context[0]["Pkg"] = "Pm"
            Package = "Premium"
    except:
        Context = None
    
    if request.method == "POST":
        Id_User = request.user.id
        body = json.loads(request.body)
        print('Data is', body)
    #try:
        Split_string = str(body["id"]).split("_",2)
        print(Split_string)
        Pkg = Split_string[0]
        User_Receiver = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Split_string[1])).values("User")[0]["User"]
        User_Recipent = Account.objects.get(id = User_Receiver)
        User_Name_Sender = Influencer_Details.objects.all().filter(User = Id_User).values("First_Name")[0]["First_Name"]
        notify.send(request.user,recipient= User_Recipent, verb= "{} Purchased Your {} Package, A project has been created Due to That!".format(User_Name_Sender,Pkg))
        Checkout_obj = Checkout_Data(User_id =Id_User,Ordered_Product = Split_string[1], Order_Product_Type = Split_string[0])
        Checkout_obj.save()
        Notify_Data = Notification_Data(Sender_id = Id_User, Receiver_id = User_Receiver, Topic = str(User_Name_Sender + "Purchased Your {} Package, A project has been created Due to That!".format(Pkg)))
        Notify_Data.save()
        Prject_obj = Project_Creation(Created_For = User_Receiver, Created_By = Id_User, Product_Id = Split_string[1],Product_Type = Split_string[0],is_Completed = False,Payment_Made =True,Payment_Released = False,Is_Delivery_Time = False, Is_Pyament_Released = False, Is_Payment_peding = False, Is_Disputed = False, Is_Realesed_Requested = False,Is_Proof_Url = False)
        Prject_obj.save()
        return redirect("/Gig")
    else:
        return render(request,"Payment.html",{"Context_Data":Context,"Pkg_Id":id,"Split1":Split_Str[0]})

def Checkout_Pay(request, id):
    pass
    


def Completeorder(request):
    body = json.loads(request.body)
    print('Data is', body)
    Split_string = str(body["id"]).split("_",2)
    return JsonResponse('payment completed!',safe=False)



