from Checkout.models import Project_Creation
from App.models import Initial_Data, Pkg_Form_Data



def Find_Product(Id):
    try:
        List_BSC = []
        List_Std = []
        List_Prm = []
        Product = Project_Creation.objects.all().filter(Product_Id = int(Id)).values("Product_Type","is_Completed")
        if Product[0]["is_Completed"] == False and Product[0]["Product_Type"] == "Basic" :
            Product_Details_Bs = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Id)).values("Besic_Packages_Descriptions","Besic_Packages_Price","Besic_Delivery_Time","Besic_Packages_Name",
            "Instagram_Image_to_Feed_Besic","Instagram_Video_to_Feed_Besic","Instagram_Post_to_Story_Besic","Instagram_Post_to_Reel_Besic","Instagram_Live_Product_Endorsment_Besic",
            "TikTok_Post_to_Feed_Besic","TikTok_Post_Product_Review_Video_Besic","TikTok_Product_Review_Short_Video_Besic","TikTok_Live_Product_Review_Besic")
            Product_Type = "Besic"
            List_BSC.append([Product_Details_Bs,Product_Type ])
            return List_BSC

        elif Product[0]["is_Completed"] == False and Product[0]["Product_Type"] == "std":
            Product_Details_Std = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Id)).values("Standered_Packages_Descriptions","Standered_Packages_Price","Standered_Delivery_Time","Standered_Packages_Name",
            "Instagram_Image_to_Feed_Std","Instagram_Video_to_Feed_Std","Instagram_Post_to_Story_Std","Instagram_Post_to_Reel_Std","Instagram_Live_Product_Endorsment_Std",
            "TikTok_Post_to_Feed_Std","TikTok_Post_Product_Review_Video_Std","TikTok_Product_Review_Short_Video_Std","TikTok_Live_Product_Review_Std")
            Product_Type = "Standered"
            List_Std.append([Product_Details_Std, Product_Type])
            return List_Std

        elif Product[0]["is_Completed"] == False and Product[0]["Product_Type"] =="pm" :
            Product_Details_Pm = Pkg_Form_Data.objects.all().filter(Gig_Id = int(Id)).values("Premium_Packages_Descriptions","Premium_Packages_Price","Premium_Delivery_Time","Premium_Packages_Name",
            "Instagram_Image_to_Feed_Prm","Instagram_Video_to_Feed_Prm","Instagram_Post_to_Story_Prm","Instagram_Post_to_Reel_Prm","Instagram_Live_Product_Endorsment_Prm",
            "TikTok_Post_to_Feed_Prm","TikTok_Post_Product_Review_Video_Prm","TikTok_Product_Review_Short_Video_Prm","TikTok_Live_Product_Review_Prm")
            Product_Type = "Premium"
            List_Prm.append([Product_Details_Pm, Product_Type])
            return List_Prm
            
        else:
            return None
    except:
        return None

def Find_Legit_User_Offer(Product, User):
    try:
        Project_ID = Project_Creation.objects.all().filter(Product_Id = Product).values("Created_For","Created_By")
        Advertiser = Project_ID[0]["Created_By"]
        Influencer = Project_ID[0]["Created_For"]
        if Advertiser == User:
            return "Adv"
        elif Influencer == User:
            return "Inf"
        else:
            return None
    except:
        return None
