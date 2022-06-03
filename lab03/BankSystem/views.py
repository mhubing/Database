import re
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.db import models

from django.views.decorators.csrf import csrf_exempt

from .models import Client, Contact, Staff

def home(request):
    
    return HttpResponse("need to finish HtteRequestRediction.")
    

@csrf_exempt
def clients(request):

    # 获取全部客户信息，显示在前端
    if request.method == "GET":
        clients = Client.objects.all()
        # context = {'clients':clients}
        contacts = Contact.objects.all()
        context = {'clients':clients, 'contacts': contacts}
        return render(request, 'BankSystem/clients.html', context)
    
    # 根据查询框输入显示输出
    if request.method == "POST":
        client_id=request.POST.get('client_id')
        client_name=request.POST.get('client_name')
        if not client_id:
            query_id = Client.objects.all()
        else:
            query_id = Client.objects.filter(id = client_id)
        if not client_name:
            query_name = Client.objects.all()
        else:
            query_name = Client.objects.filter(name = client_name)
        clients = query_id & query_name
        context = {'clients':clients}
        return render(request, 'BankSystem/clients.html', context)


@csrf_exempt
def add_client(request):
    # 在数据库中插入数据
    if request.method == "POST":
        client_id=request.POST.get('client_id')
        if Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_client.html', {'error': '该用户已存在'})
        if not client_id:
            return render(request, 'BankSystem/add_client.html', {'error': '输入不能为空'})

        client_name=request.POST.get('client_name')
        client_phone=request.POST.get('client_phone')
        client_address=request.POST.get('client_address')
        client_staff_id=request.POST.get("client_staff_id")
        client_staff_type=request.POST.get("client_staff_type")
        
        Client.objects.create(
            id = client_id,
            name = client_name,
            phone = client_phone,
            address = client_address,
            staff_id = Staff.objects.get(id=client_staff_id),
            staff_type = client_staff_type,
        )
        return redirect('./clients')
    return render(request, 'BankSystem/add_client.html')


@csrf_exempt
def del_client(request, client_id):
    if request.method == "GET":
        obj_list = Client.objects.filter(id=client_id)
        if not obj_list:
            return HttpResponse("该用户不存在")
        obj_list.delete()
        return redirect('../../clients')
    return render(request, 'BankSystem/clients.html', {'error': '删除失败'})


@csrf_exempt
def edit_client(request, client_id):
    obj_list = Client.objects.filter(id = client_id).values('id', 'name', 'phone', 'address', 'staff_id', 'staff_type')
    if not obj_list:
        return HttpResponse("该用户不存在")
    obj=obj_list[0] # 对其中一个数据进行编辑

    if request.method == "POST":
        Client.objects.all().filter(id=client_id).update(
            name=request.POST.get('client_name'),
            phone=request.POST.get('client_phone'),
            address=request.POST.get('client_address'),
            staff_id = Staff.objects.get(id=request.POST.get("client_staff_id")),
            staff_type = request.POST.get('client_staff_type')
        )
        return redirect('../../clients')
    return render(request, 'BankSystem/edit_client.html', {'obj' : obj})


# 管理客户联系人
@csrf_exempt
def contacts(request, client_id):
    # if request.method == "GET":
    obj_list = Client.objects.filter(id=client_id)
    print("client_id: ", client_id)
    if not obj_list:
        return HttpResponse("该用户不存在")
    contacts = Contact.objects.filter(client_id = client_id)
    context = {'contacts':contacts, 'client_id':client_id}

    if request.method == "POST":
        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        contact_relation = request.POST.get("contact_relation")
        
        Contact.objects.create(
            client_id = Client.objects.get(id=client_id),
            name = contact_name,
            phone = contact_phone,
            email = contact_email,
            relation = contact_relation,
        )
    
    return render(request, 'BankSystem/contacts.html', context)


        
    


def accounts(request):
    return HttpResponse("need to finish account management.")

def loans(request):
    return HttpResponse("need to finish loan management.")

def statistics(request):
    return HttpResponse("need to finish business statistics.")

