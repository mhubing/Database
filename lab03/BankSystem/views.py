import email
from http import client
from django.shortcuts import redirect, render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from .models import AccessAccount, Account, Client, Contact, Staff


def home(request):
    
    return HttpResponse("need to finish HtteRequestRediction.")
    

@csrf_exempt
def clients(request):

    # 获取全部客户信息，显示在前端
    if request.method == "GET":
        clients = Client.objects.all()
        context = {'clients':clients}
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
        if not client_id:
            return render(request, 'BankSystem/add_client.html', {'error': '输入不能为空'})
        if Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_client.html', {'error': '该用户已存在'})

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
        
        account_list = AccessAccount.objects.filter(client_id=client_id)
        if account_list:
            return HttpResponse("该用户存在关联账户，不能删除")
        obj_list.delete()
        return redirect('../../clients')
    return render(request, 'BankSystem/clients.html', {'error': '删除失败'})


@csrf_exempt
def edit_client(request, client_id):
    obj_list = Client.objects.filter(id = client_id).values('id', 'name', 'phone', 'address', 'staff_id', 'staff_type')
    if not obj_list:
        return HttpResponse("该用户不存在")
    obj=obj_list[0]

    contacts=Contact.objects.filter(client_id = client_id)
    if contacts:
        return HttpResponse("该用户存在关联信息，不能修改身份证号")

    if request.method == "POST":
        Client.objects.all().filter(id=client_id).update(
            id=request.POST.get('client_id'),
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
    if request.method == "GET":
        obj_list = Client.objects.filter(id=client_id)
        if not obj_list:
            return HttpResponse("该用户不存在")
        contacts = Contact.objects.filter(client_id = client_id)
        context = {'contacts':contacts, 'client_id': client_id}
        return render(request, 'BankSystem/contacts.html', context)
    # 查询
    if request.method == "POST":
        contact_name=request.POST.get('contact_name')
        print("contact_name: ", contact_name)
        if not contact_name:
            contacts = Contact.objects.filter(client_id = client_id)
        else:
            contacts = Contact.objects.filter(**{'name':contact_name, 'client_id':client_id})
        context = {'contacts':contacts, 'client_id': client_id}
        return render(request, 'BankSystem/contacts.html', context)


@csrf_exempt
def add_contact(request, client_id):
    obj_list = Client.objects.filter(id=client_id)
    if not obj_list:
        return HttpResponse("该用户不存在")    

    if request.method == "POST":
        contact_name = request.POST.get('contact_name')
        if not contact_name:
            return render(request, 'BankSystem/add_contact.html', {'error': '输入不能为空', 'client_id': client_id})
        if Contact.objects.filter(**{'name':contact_name, 'client_id':client_id}):
            return render(request, 'BankSystem/add_contact.html', {'error': '该联系人已存在', 'client_id': client_id})
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
        # return redirect('../contacts')
        url = '/clients/contacts/'+client_id
        return HttpResponseRedirect(url)
    return render(request, 'BankSystem/add_contact.html', {'client_id': client_id})

    
@csrf_exempt
def del_contact(request, client_id, contact_name):
    if request.method == "GET":
        obj_list = Client.objects.filter(id=client_id)
        if not obj_list:
            return HttpResponse("该用户不存在")
        contacts = Contact.objects.filter(**{'client_id': client_id, 'name': contact_name})
        if not contacts:
            return HttpResponse("该联系人不存在")

        contacts.delete()
        url = '/clients/contacts/'+client_id
        return HttpResponseRedirect(url)
    return render(request, 'BankSystem/contacts.html', {'client_id': client_id, 'error': '删除失败'})


@csrf_exempt
def edit_contact(request, client_id, contact_name):
    obj_list = Client.objects.filter(id = client_id)
    if not obj_list:
        return HttpResponse("该用户不存在")
    obj_list = Contact.objects.filter(**{'name':contact_name, 'client_id':client_id}).values('client_id', 'name', 'phone', 'email', 'relation')
    if not obj_list:
        return HttpResponse("该联系人不存在")
    obj = obj_list[0]
    
    if request.method == "POST":
        contact_name_=request.POST.get('contact_name')
        if not contact_name_:
            return render(request, 'BankSystem/edit_contact.html', {'error': '输入不能为空', 'client_id': client_id, 'contact_name':contact_name})
        contact_phone=request.POST.get('contact_phone')
        contact_email=request.POST.get('contact_email')
        contact_relation = request.POST.get('contact_relation')
        Contact.objects.all().filter(**{'name':contact_name, 'client_id':client_id}).update(
            name=contact_name_,
            phone=contact_phone,
            email=contact_email,
            relation=contact_relation,
        )
        url = '/clients/contacts/'+client_id
        return HttpResponseRedirect(url)
    return render(request, 'BankSystem/edit_contact.html', {'obj':obj, 'client_id': client_id, 'contact_name':contact_name})




def accounts(request):
    # 获取全部客户信息，显示在前端
    if request.method == "GET":
        accounts = Account.objects.all()
        context = {'accounts':accounts}
        return render(request, 'BankSystem/clients.html', context)

    return HttpResponse("need to finish account management.")


def loans(request):
    return HttpResponse("need to finish loan management.")

def statistics(request):
    return HttpResponse("need to finish business statistics.")

