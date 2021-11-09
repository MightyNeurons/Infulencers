from django.shortcuts import render

# Create your views here.


def Notification(request,id):
    return render(request,'notification.html')