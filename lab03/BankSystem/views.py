from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.db import models

from .models import Client

def home(request):
    
    return HttpResponse("need to finish HtteRequestRediction.")

def clients(request):
    if request.method == "POST":
        new_client = models.send(
            client_id=request.POST.get("id"),
            client_name=request.POST.get("name"),
            client_phone=request.POST.get("phone"),
            client_address=request.POST.get("address"),
            client_staff_id=request.POST.get("staff_id"),
            client_staff_type=request.POST.get("staff_type")
        )
        new_client.save()
        print("新增客户：",new_client)
        return redirect('../')

    clients = Client.objects.all()
    # clients = [
    #     {'id':'231', 'name':'user1', 'phone':"123456", 'address':'xinhua'}
    # ]
    context = {'clients':clients}
    return render(request, 'BankSystem/clients.html', context)
   
    # return HttpResponse("need to finish client management.")

def accounts(request):
    return HttpResponse("need to finish account management.")

def loans(request):
    return HttpResponse("need to finish loan management.")

def statistics(request):
    return HttpResponse("need to finish business statistics.")

