from Checkout.models import Project_Creation
from .models import Account





def Get_Project_Id(Id):
    List =[]

    try:
        Project_Id = Project_Creation.objects.all().filter(Created_For = Id).values("Product_Id","Product_Type","is_Completed")
        if Project_Id is not None:
            for i in range(len(Project_Id)):
                if Project_Id[i]["is_Completed"] == False:
                    List.append([Project_Id[i]["Product_Id"], Project_Id[i]["Product_Type"]])
            
            return List
        else:
            return None
    except:
        return None

def Get_Recipent_User():
    User_Recipent = []
    Id_All = Account.objects.all().values("id")
    for i in range(len(Id_All)):
        User_Recipent.append(Account.objects.get(id = Id_All[i]["id"]))
    return User_Recipent
