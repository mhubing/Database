from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.db import models

from django.views.decorators.csrf import csrf_exempt

from .models import Client, Staff

def home(request):
    
    return HttpResponse("need to finish HtteRequestRediction.")
    

def clients(request):

    # 获取全部客户信息，显示在前端
    if request.method == "GET":
        clients = Client.objects.all()
        context = {'clients':clients}
        return render(request, 'BankSystem/clients.html', context)
        
    # return HttpResponse("need to finish client management.")

@csrf_exempt
def add_client(request):
    # 在数据库中插入数据
    if request.method == "POST":
        client_id=request.POST.get('id')
        if Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_client.html', {'error': '该用户已存在'})
        if not client_id:
            return render(request, 'BankSystem/add_client.html', {'error': '输入不能为空'})

        client_name=request.POST.get('name')
        client_phone=request.POST.get('phone')
        client_address=request.POST.get('address')
        # client_staff_id=request.POST.get("staff_id"),
        # client_staff_type=request.POST.get("staff_type")
        
        Client.objects.create(
            id = client_id,
            name = client_name,
            phone = client_phone,
            address = client_address,
            # staff_id_id = client_staff_id,
            # staff_type = client_staff_type
        )
        return redirect('./clients')
    return render(request, 'BankSystem/add_client.html')


def accounts(request):
    return HttpResponse("need to finish account management.")

def loans(request):
    return HttpResponse("need to finish loan management.")

def statistics(request):
    return HttpResponse("need to finish business statistics.")

