from http import client
from locale import currency
from multiprocessing.dummy import current_process
from decimal import Decimal
from re import L
from typing import overload
from django.shortcuts import redirect, render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear

from .models import AccessAccount, Account, CheckingAccount, Client, Contact, SavingsAccount, Staff, Subbranch, SubbranchClientAccountType, Loan, PayLoan, ClientLoan


def home(request):
    
    return render(request, 'BankSystem/home.html')
    

"""------------------客户管理------------------"""
# 1.客户视图（包括查询）
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

# 2.增加客户视图
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
        if Client.objects.filter(phone = client_phone):
            return render(request, 'BankSystem/add_client.html', {'error_ph': '该号码已存在'})
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
        return redirect('../clients')
    return render(request, 'BankSystem/add_client.html')

# 3.删除客户视图
@csrf_exempt
def del_client(request, client_id):
    if request.method == "GET":
        obj_list = Client.objects.filter(id=client_id)
        if not obj_list:
            return HttpResponse("该用户不存在")
        
        account_list = SubbranchClientAccountType.objects.filter(client_id=client_id)
        if account_list:
            return HttpResponse("该用户存在关联账户，不能删除")
        obj_list.delete()
        return redirect('../../clients')
    return HttpResponse('删除失败')

# 4.编辑客户视图
@csrf_exempt
def edit_client(request, client_id):
    obj_list = Client.objects.filter(id = client_id).values('id', 'name', 'phone', 'address', 'staff_id', 'staff_type')
    if not obj_list:
        return HttpResponse("该用户不存在")
    obj=obj_list[0]

    if request.method == "POST":
        new_client_id = request.POST.get('client_id')
        if (new_client_id != client_id) and Contact.objects.filter(client_id = client_id):
            return render(request, 'BankSystem/edit_client.html', {'obj' : obj, 'error': '该用户有关联信息，不能修改身份证号'})
        if (new_client_id != client_id) and Client.objects.filter(id=new_client_id):
            return render(request, 'BankSystem/edit_client.html', {'obj' : obj, 'error': '该身份证号已存在'})

        with transaction.atomic():
            Client.objects.all().filter(id=client_id).update(
                id=new_client_id,
                name=request.POST.get('client_name'),
                phone=request.POST.get('client_phone'),
                address=request.POST.get('client_address'),
                staff_id = Staff.objects.get(id=request.POST.get("client_staff_id")),
                staff_type = request.POST.get('client_staff_type')
            )
        return redirect('../../clients')
    return render(request, 'BankSystem/edit_client.html', {'obj' : obj})


"""------------------客户联系人管理------------------"""
# 5.一个客户的联系人视图（包括查询）
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
        if not contact_name:
            contacts = Contact.objects.filter(client_id = client_id)
        else:
            contacts = Contact.objects.filter(**{'name':contact_name, 'client_id':client_id})
        context = {'contacts':contacts, 'client_id': client_id}
        return render(request, 'BankSystem/contacts.html', context)

# 6.增加客户联系人视图
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
        if Contact.objects.filter(**{'phone':contact_phone}):
            return render(request, 'BankSystem/add_contact.html', {'error_ph': '该号码已存在', 'client_id': client_id})
        contact_email = request.POST.get('contact_email')
        if Contact.objects.filter(**{'email':contact_email}):
            return render(request, 'BankSystem/add_contact.html', {'error_em': '该email已存在', 'client_id': client_id})
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

# 7.删除客户联系人视图
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
    return HttpResponse('删除失败')

# 8.编辑客户联系人视图
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


"""------------------账户管理------------------"""
# 9.账户视图（包括查询）
@csrf_exempt
def accounts(request):
    # 获取全部账户信息，显示在前端
    if request.method == "GET":
        accounts = Account.objects.all()
        accessaccounts = AccessAccount.objects.all()
        return render(request, 'BankSystem/accounts.html', {'accounts':accounts, 'accessaccounts':accessaccounts})
    # 查询
    # TODO:根据用户id查询account
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        client_id = request.POST.get('client_id')
        if not account_id:
            query_account = Account.objects.all()
            query_account_aa = AccessAccount.objects.all()
        else:
            query_account = Account.objects.filter(id=account_id)
            query_account_aa = AccessAccount.objects.filter(account_id=account_id)
        if not client_id:
            query_client_aa = AccessAccount.objects.all()
        else:
            query_client_aa = AccessAccount.objects.filter(client_id=client_id)
        
        accounts = query_account
        accessaccounts = query_account_aa & query_client_aa
        return render(request, 'BankSystem/accounts.html', {'accounts':accounts, 'accessaccounts':accessaccounts})
        
    return HttpResponse("need to finish account management.")

# 10.增加支票账户视图
@csrf_exempt
def add_checking(request):
    if request.method == "POST":
        subbranch_name = request.POST.get('subbranch_name')
        if not subbranch_name:
            return render(request, 'BankSystem/add_checking.html', {'error_sn': '输入不能为空'})
        if not Subbranch.objects.filter(name = subbranch_name):
            return render(request, 'BankSystem/add_checking.html', {'error_sn': '该支行不存在'})
        
        client_id = request.POST.get('client_id')
        if not client_id:
            return render(request, 'BankSystem/add_checking.html', {'error_ci': '输入不能为空'})
        if not Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_checking.html', {'error_ci': '该客户不存在'})

        account_id = request.POST.get('account_id')
        if not account_id:
            return render(request, 'BankSystem/add_checking.html', {'error_ai': '输入不能为空'})
        if Account.objects.filter(id = account_id):
            return render(request, 'BankSystem/add_checking.html', {'error_ai': '该账户已存在'})

        if SubbranchClientAccountType.objects.filter(**{'subbranch_name': subbranch_name, 'client_id': client_id, 'account_type': 'checking_account'}):
            return render(request, 'BankSystem/add_checking.html', {'error_scat': '客户在该支行已拥有支票账户'})

        open_day = request.POST.get('open_day')
        account_balance = request.POST.get('account_balance')
        account_overdraft = request.POST.get('account_overdraft')

        with transaction.atomic():
            Account.objects.create(
                id = account_id,
                balance = account_balance,
                open_date = open_day,
                type = 'checking_account',
            )
            CheckingAccount.objects.create(
                account_id = Account.objects.get(id=account_id),
                overdraft = account_overdraft,
            )
            SubbranchClientAccountType.objects.create(
                subbranch_name = Subbranch.objects.get(name=subbranch_name),
                client_id = Client.objects.get(id=client_id),
                account_id = Account.objects.get(id=account_id),
                account_type = 'checking_account'
            )
            AccessAccount.objects.create(
                account_id = Account.objects.get(id=account_id),
                client_id = Client.objects.get(id=client_id),
                least_recently_access = open_day,
            )

        return redirect('../accounts')
    return render(request, 'BankSystem/add_checking.html')

# 11.增加储蓄账户视图
# 此时只允许添加一位客户
@csrf_exempt
def add_savings(request):
    if request.method == "POST":
        subbranch_name = request.POST.get('subbranch_name')
        if not subbranch_name:
            return render(request, 'BankSystem/add_savings.html', {'error_sn': '输入不能为空'})
        if not Subbranch.objects.filter(name = subbranch_name):
            return render(request, 'BankSystem/add_savings.html', {'error_sn': '该支行不存在'})
        
        client_id = request.POST.get('client_id')
        if not client_id:
            return render(request, 'BankSystem/add_savings.html', {'error_ci': '输入不能为空'})
        if not Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_savings.html', {'error_ci': '该客户不存在'})

        account_id = request.POST.get('account_id')
        if not account_id:
            return render(request, 'BankSystem/add_savings.html', {'error_ai': '输入不能为空'})
        if Account.objects.filter(**{'id': account_id}):
            return render(request, 'BankSystem/add_savings.html', {'error_ai': '该账户已存在'})

        if SubbranchClientAccountType.objects.filter(**{'subbranch_name': subbranch_name, 'client_id': client_id, 'account_type': 'savings_account'}):
            return render(request, 'BankSystem/add_savings.html', {'error_scat': '客户在该支行已拥有储蓄账户'})

        open_day = request.POST.get('open_day')
        account_balance = request.POST.get('account_balance')
        interest_rate = request.POST.get('interest_rate')
        currency_type = request.POST.get('currency_type')

        with transaction.atomic():
            Account.objects.create(
                id = account_id,
                balance = account_balance,
                open_date = open_day,
                type = 'savings_account',
            )
            SavingsAccount.objects.create(
                account_id = Account.objects.get(id=account_id),
                interest_rate = interest_rate,
                currency_type = currency_type,
            )
            SubbranchClientAccountType.objects.create(
                subbranch_name = Subbranch.objects.get(name=subbranch_name),
                client_id = Client.objects.get(id=client_id),
                account_id = Account.objects.get(id=account_id),
                account_type = 'savings_account'
            )
            AccessAccount.objects.create(
                client_id = Client.objects.get(id=client_id),
                account_id = Account.objects.get(id=account_id),
                least_recently_access = open_day,
            )

        return redirect('../accounts')
    return render(request, 'BankSystem/add_savings.html')

# 12.删除账户视图
@csrf_exempt
def del_account(request, account_id):
    if request.method == "GET":
        accounts=Account.objects.filter(id=account_id)
        accessaccounts = AccessAccount.objects.filter(account_id=account_id)
        obj_list = Account.objects.filter(id=account_id).values('id', 'balance', 'open_date', 'type')
        if not obj_list:
            return HttpResponse("该账户不存在")
        if obj_list[0]['type'] == 'checking_account' and obj_list[0]['balance'] < 0:
            return render(request, 'BankSystem/accounts.html', {'error_del': '透支额未付清，删除支票帐户失败', 'accounts': accounts, 'accessaccounts': accessaccounts})

        with transaction.atomic():
            Account.objects.filter(id=account_id).delete()
            SavingsAccount.objects.filter(account_id=account_id).delete()
            CheckingAccount.objects.filter(account_id=account_id).delete()
            SubbranchClientAccountType.objects.filter(**{'account_id': account_id}).delete()
            AccessAccount.objects.filter(account_id=account_id).delete()

        return redirect('../../accounts')
    return HttpResponse('删除失败')

# 13.编辑账户视图
# 默认只显示一位客户
@csrf_exempt
def edit_account(request, account_id):
    obj_list = Account.objects.filter(id=account_id)
    if not obj_list:
        return HttpResponse("该帐号不存在")
    obj=obj_list.first()
    # 涉及到先反向查询，再正向
    subbranch_list = Account.objects.get(id=account_id)
    subbranch = subbranch_list.subbranchclientaccounttype_set.all().first().subbranch_name
    client_list = Account.objects.get(id=account_id)
    client = client_list.subbranchclientaccounttype_set.all().first().client_id

    if(request.method=="POST"):
        account_balance = request.POST.get('account_balance')
        account_overdraft = request.POST.get('account_overdraft')
        lsa = request.POST.get('least_recently_access')
        if obj.type == 'checking_account':
            # fabs(余额) < 透支额度
            if Decimal(account_balance) < Decimal(0) and Decimal(account_balance) + Decimal(account_overdraft) < 0:
                return HttpResponse("欠款超过透支额度，修改失败")
            with transaction.atomic():
                Account.objects.all().filter(id=account_id).update(
                    balance = account_balance,
                )
                CheckingAccount.objects.all().filter(account_id=account_id).update(
                    overdraft = account_overdraft,
                )
                AccessAccount.objects.all().filter(account_id=account_id).update(
                    least_recently_access = lsa,
                )
        if obj.type == 'savings_account':
            if Decimal(account_balance) < Decimal(0):
                return HttpResponse("储蓄账户不能透支")
            with transaction.atomic():
                Account.objects.all().filter(id=account_id).update(
                    balance = account_balance,
                )
                SavingsAccount.objects.all().filter(account_id=account_id).update(
                    interest_rate = request.POST.get('interest_rate'),
                    currency_type = request.POST.get('currency_type'),
                )
                AccessAccount.objects.all().filter(account_id=account_id).update(
                    least_recently_access = lsa,
                )
        return redirect('../../accounts')
    return render(request, 'BankSystem/edit_account.html', {'obj':obj, 'subbranch':subbranch, 'client':client})
                    
# 14.向账户增加客户的视图
@csrf_exempt
def add_clienttoaccount(request, account_id, account_type):
    subbranch_list = Account.objects.get(id=account_id)
    subbranch = subbranch_list.subbranchclientaccounttype_set.all().first().subbranch_name

    if request.method == "POST":
        client_id = request.POST.get('client_id')
        if not Client.objects.filter(id=client_id):
            return render(request, 'BankSystem/add_clienttoaccount.html', {'error':'该客户不存在', 'subbranch':subbranch, 'account_id': account_id})
        if SubbranchClientAccountType.objects.filter(**{'subbranch_name': subbranch, 'client_id': client_id, 'account_type': account_type}):
            return render(request, 'BankSystem/add_clienttoaccount.html', {'error':'该客户已拥有该类型账户', 'subbranch':subbranch, 'account_id': account_id})

        lra = request.POST.get('lra')
        with transaction.atomic():
            AccessAccount.objects.create(
                account_id = Account.objects.get(id=account_id),
                client_id = Client.objects.get(id=client_id),
                least_recently_access = lra,
            )
            SubbranchClientAccountType.objects.create(
                subbranch_name = subbranch,
                client_id = Client.objects.get(id=client_id),
                account_id = Account.objects.get(id=account_id),
                account_type = account_type,
            )
        return redirect('../../../accounts')

    return render(request, 'BankSystem/add_clienttoaccount.html', {'subbranch':subbranch, 'account_id': account_id})

# 15.删除账户的一个客户
@csrf_exempt
def del_clienttoaccount(request, account_id, client_id):
    if request.method == "GET":
        accounts=Account.objects.filter(id=account_id)
        accessaccounts = AccessAccount.objects.filter(account_id=account_id)
        if not Account.objects.filter(id=account_id):
            return HttpResponse("该账户不存在")
        if not Client.objects.filter(id=client_id):
            return HttpResponse("该客户不存在")
        if not SubbranchClientAccountType.objects.filter(**{'client_id':client_id, 'account_id':account_id}):
            return HttpResponse("该账户不属于该客户")
        
        if Client.objects.filter(id=client_id).count()==1:
            return render(request, 'BankSystem/accounts.html', {'error_del_c': '该账户仅有一个客户，不运行进行客户删除', 'accounts': accounts, 'accessaccounts': accessaccounts})

        with transaction.atomic():
            AccessAccount.objects.filter(**{'client_id':client_id, 'account_id':account_id}).delete()
            SubbranchClientAccountType.objects.filter(**{'client_id':client_id, 'account_id':account_id}).delete()
        return redirect('../../../accounts')
            
    return HttpResponse('删除失败')


"""------------------贷款管理------------------"""
# 16.贷款视图
@csrf_exempt
def loans(request):
    # 获取贷款信息，显示在前端
    if request.method == "GET":
        loans = Loan.objects.all()
        payloans = PayLoan.objects.all()
        clientloans = ClientLoan.objects.all()
        return render(request, 'BankSystem/loans.html', {'loans':loans, 'payloans':payloans, "clientloans":clientloans})
    # 查询
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')
        client_id = request.POST.get('client_id')
        if not loan_id:
            query_loans_li = Loan.objects.all()
            query_payloans_li= PayLoan.objects.all()
            query_clientloans_li = ClientLoan.objects.all()
        else:
            loan=Loan.objects.filter(id=loan_id)
            query_loans_li = Loan.objects.filter(id=loan_id)
            query_payloans_li= PayLoan.objects.filter(loan__in=loan)
            query_clientloans_li = ClientLoan.objects.filter(loan__in=loan)

        if not client_id:
            query_clientloans_ci= ClientLoan.objects.all()
        else:
            client=Client.objects.filter(id=client_id)
            query_clientloans_ci = ClientLoan.objects.filter(client__in=client)
        
        loans = query_loans_li
        payloans = query_payloans_li
        clientloans = query_clientloans_li & query_clientloans_ci
        return render(request, 'BankSystem/loans.html', {'loans':loans, 'payloans':payloans, "clientloans":clientloans})
       

    return HttpResponse("need to finish loan management.")

# 17.新增贷款视图
@csrf_exempt
def add_loan(request):
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')
        if not loan_id:
            return render(request, 'BankSystem/add_loan.html', {'error_li': '输入不能为空'})
        if Loan.objects.filter(id=loan_id):
            return render(request, 'BankSystem/add_loan.html', {'error_li': '该贷款号已存在'})

        subbranch_name = request.POST.get('subbranch_name')
        if not subbranch_name:
            return render(request, 'BankSystem/add_loan.html', {'error_sn': '输入不能为空'})
        if not Subbranch.objects.filter(name = subbranch_name):
            return render(request, 'BankSystem/add_loan.html', {'error_sn': '该支行不存在'})

        client_id = request.POST.get('client_id')
        if not client_id:
            return render(request, 'BankSystem/add_loan.html', {'error_ci': '输入不能为空'})
        if not Client.objects.filter(id = client_id):
            return render(request, 'BankSystem/add_loan.html', {'error_ci': '该客户不存在'})

        loan_amount = request.POST.get('loan_amount')
        if not loan_amount:
            return render(request, 'BankSystem/add_loan.html', {'error_la': '输入不能为空'})
        
        with transaction.atomic():
            Loan.objects.create(
                id = loan_id,
                subbranch = Subbranch.objects.get(name=subbranch_name),
                amount = loan_amount,
                status = 'unissue',
            )
            ClientLoan.objects.create(
                loan = Loan.objects.get(id=loan_id),
                client = Client.objects.get(id=client_id),
            )
        
        return redirect('../loans')
    return render(request, 'BankSystem/add_loan.html')

# 18.给贷款增加客户
@csrf_exempt
def add_clientloan(request, loan_id):
    subbranch = Loan.objects.get(id=loan_id).subbranch
    if request.method == "POST":
        client_id = request.POST.get('client_id')
        if not client_id:
            return render(request, 'BankSystem/add_clientloan.html', {'error': '输入不能为空'})
        if not Client.objects.filter(id=client_id):
            return render(request, 'BankSystem/add_clientloan.html', {'error_ci': '该客户不存在'})

        ClientLoan.objects.create(
            loan = Loan.objects.get(id=loan_id),
            client = Client.objects.get(id=client_id),
        )
        return redirect('../../loans')
    return render(request, 'BankSystem/add_clientloan.html', {'subbranch':subbranch, 'loan_id': loan_id})

# 19.发放贷款
@csrf_exempt
def payloan(request, loan_id):
    loan_status = Loan.objects.get(id=loan_id).status
    loans = Loan.objects.all()
    payloans = PayLoan.objects.all()
    clientloans = ClientLoan.objects.all()
    if loan_status == 'issued':
        return render(request, 'BankSystem/loans.html', {'error_del': '该贷款已经全部发放', 'loans':loans, 'payloans':payloans, "clientloans":clientloans})
    if request.method == "POST":
        pay_date = request.POST.get('pay_date')
        pay_amount = request.POST.get('pay_amount')
        if Decimal(pay_amount) <= Decimal(0):
            return render(request, 'BankSystem/payloan.html', {'error_pa': '支付金额错误', 'loan_id': loan_id})

        payloan_list = PayLoan.objects.filter(loan=Loan.objects.get(id=loan_id))
        if payloan_list:
            total_pay = Decimal(pay_amount)+Decimal(payloan_list.aggregate(Sum('pay_amount'))['pay_amount__sum'])
        else:
            total_pay = Decimal(pay_amount)
        if total_pay > Loan.objects.get(id=loan_id).amount:
            return render(request, 'BankSystem/payloan.html', {'error_pa': '支付金额超出贷款额度', 'loan_id': loan_id})
        elif total_pay == Loan.objects.get(id=loan_id).amount:
            loan_status = 'issued'
        else:
            loan_status = 'issuing'

        with transaction.atomic():
            PayLoan.objects.create(
                loan = Loan.objects.get(id=loan_id),
                pay_date = pay_date,
                pay_amount = pay_amount,
            )
            Loan.objects.filter(id=loan_id).update(
                status = loan_status,
            )
        return redirect('../../loans')
    return render(request, 'BankSystem/payloan.html', {'loan_id': loan_id})

# 20.删除贷款
@csrf_exempt
def del_loan(request, loan_id):
    loans = Loan.objects.all()
    payloans = PayLoan.objects.all()
    clientloans = ClientLoan.objects.all()
    if request.method == "GET":
        loan_status = Loan.objects.get(id=loan_id).status
        if loan_status=='issuing':
            return render(request, 'BankSystem/loans.html', {'error_del': '该贷款正在支付中，无法删除', 'loans':loans, 'payloans':payloans, "clientloans":clientloans})
        loan = Loan.objects.filter(id=loan_id)

        with transaction.atomic():
            PayLoan.objects.filter(loan__in=loan).delete()
            Loan.objects.filter(id=loan_id).delete()

        return redirect('../../loans')
    return HttpResponse('删除失败')


"""------------------业务统计------------------"""
# 业务统计视图
def statistics(request):
    hefei_branch = Subbranch.objects.filter(name='HeFei Subbranch')
    nanyang_branch = Subbranch.objects.filter(name='nanyang Subbranch')

    # 储蓄-合肥支行
    accounts_hefei = SubbranchClientAccountType.objects.filter(subbranch_name__in=hefei_branch).values('account_id')
    savings_accounts = SavingsAccount.objects.filter(account_id__in=accounts_hefei).values('account_id')
    # 储蓄-合肥支行-月
    savings_hefei_month = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(month=TruncMonth('least_recently_access')).values('month') \
        .values('account_id')
    
    savings_hefei_amount = Account.objects.filter(id__in=savings_hefei_month) \
        .aggregate(month_amount=Sum('balance'))
    savings_hefei_client = SubbranchClientAccountType.objects.filter(account_id__in=savings_hefei_month) \
        .aggregate(month_clients=Count('client_id'))

    # 储蓄-合肥支行-季
    savings_hefei_quarter = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(quarter=TruncQuarter('least_recently_access')).values('quarter') \
        .values('account_id')
    
    savings_hefei_amount.update(Account.objects.filter(id__in=savings_hefei_quarter) \
        .aggregate(quarter_amount=Sum('balance')))
    savings_hefei_client.update(SubbranchClientAccountType.objects.filter(account_id__in=savings_hefei_quarter) \
        .aggregate(quarter_clients=Count('client_id')))

    # 储蓄-合肥支行-年
    savings_hefei_year = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(year=TruncYear('least_recently_access')).values('year') \
        .values('account_id')
    
    savings_hefei_amount.update(Account.objects.filter(id__in=savings_hefei_year) \
        .aggregate(year_amount=Sum('balance')))
    savings_hefei_client.update(SubbranchClientAccountType.objects.filter(account_id__in=savings_hefei_year) \
        .aggregate(year_clients=Count('client_id')))


    # 贷款-合肥支行
    loan_hefei = Loan.objects.filter(subbranch__in=hefei_branch)

    # 贷款-合肥支行-月
    loan_hefei_month = PayLoan.objects.filter(loan__in=loan_hefei) \
        .annotate(month=TruncMonth('pay_date')).values('month') \
        .values('loan')

    loan_hefei_amount = loan_hefei_month.aggregate(month_amount=Sum('pay_amount'))
    loan_hefei_client = ClientLoan.objects.filter(loan__in=loan_hefei_month) \
        .aggregate(month_clients=Count('client'))

    # 贷款-合肥支行-季
    loan_hefei_quarter = PayLoan.objects.filter(loan__in=loan_hefei) \
        .annotate(quarter=TruncQuarter('pay_date')).values('quarter') \
        .values('loan')

    loan_hefei_amount.update(loan_hefei_quarter.aggregate(quarter_amount=Sum('pay_amount')))
    loan_hefei_client.update(ClientLoan.objects.filter(loan__in=loan_hefei_quarter) \
        .aggregate(quarter_clients=Count('client')))

    # 贷款-合肥支行-年
    loan_hefei_year = PayLoan.objects.filter(loan__in=loan_hefei) \
        .annotate(year=TruncYear('pay_date')).values('year') \
        .values('loan')

    loan_hefei_amount.update(loan_hefei_year.aggregate(year_amount=Sum('pay_amount')))
    loan_hefei_client.update(ClientLoan.objects.filter(loan__in=loan_hefei_year) \
        .aggregate(year_clients=Count('client')))


    # 储蓄-南阳支行TODO:
    accounts_nanyang = SubbranchClientAccountType.objects.filter(subbranch_name__in=nanyang_branch).values('account_id')
    savings_accounts = SavingsAccount.objects.filter(account_id__in=accounts_nanyang).values('account_id')
    # 储蓄-南阳支行-月
    savings_nanyang_month = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(month=TruncMonth('least_recently_access')).values('month') \
        .values('account_id')
    
    savings_nanyang_amount = Account.objects.filter(id__in=savings_nanyang_month) \
        .aggregate(month_amount=Sum('balance'))
    savings_nanyang_client = SubbranchClientAccountType.objects.filter(account_id__in=savings_nanyang_month) \
        .aggregate(month_clients=Count('client_id'))

    # 储蓄-南阳支行-季
    savings_nanyang_quarter = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(quarter=TruncQuarter('least_recently_access')).values('quarter') \
        .values('account_id')
    
    savings_nanyang_amount.update(Account.objects.filter(id__in=savings_nanyang_quarter) \
        .aggregate(quarter_amount=Sum('balance')))
    savings_nanyang_client.update(SubbranchClientAccountType.objects.filter(account_id__in=savings_nanyang_quarter) \
        .aggregate(quarter_clients=Count('client_id')))

    # 储蓄-南阳支行-年
    savings_nanyang_year = AccessAccount.objects.filter(**{'account_id__in': savings_accounts}) \
        .annotate(year=TruncYear('least_recently_access')).values('year') \
        .values('account_id')
    
    savings_nanyang_amount.update(Account.objects.filter(id__in=savings_nanyang_year) \
        .aggregate(year_amount=Sum('balance')))
    savings_nanyang_client.update(SubbranchClientAccountType.objects.filter(account_id__in=savings_nanyang_year) \
        .aggregate(year_clients=Count('client_id')))



    # 贷款-南阳支行
    loan_nanyang = Loan.objects.filter(subbranch__in=nanyang_branch)

    # 贷款-南阳支行-月
    loan_nanyang_month = PayLoan.objects.filter(loan__in=loan_nanyang) \
        .annotate(month=TruncMonth('pay_date')).values('month') \
        .values('loan')

    loan_nanyang_amount = loan_nanyang_month.aggregate(month_amount=Sum('pay_amount'))
    loan_nanyang_client = ClientLoan.objects.filter(loan__in=loan_nanyang_month) \
        .aggregate(month_clients=Count('client'))

    # 贷款-南阳支行-季
    loan_nanyang_quarter = PayLoan.objects.filter(loan__in=loan_nanyang) \
        .annotate(quarter=TruncQuarter('pay_date')).values('quarter') \
        .values('loan')

    loan_nanyang_amount.update(loan_nanyang_quarter.aggregate(quarter_amount=Sum('pay_amount')))
    loan_nanyang_client.update(ClientLoan.objects.filter(loan__in=loan_nanyang_quarter) \
        .aggregate(quarter_clients=Count('client')))

    # 贷款-南阳支行-年
    loan_nanyang_year = PayLoan.objects.filter(loan__in=loan_nanyang) \
        .annotate(year=TruncYear('pay_date')).values('year') \
        .values('loan')

    loan_nanyang_amount.update(loan_nanyang_year.aggregate(year_amount=Sum('pay_amount')))
    loan_nanyang_client.update(ClientLoan.objects.filter(loan__in=loan_nanyang_year) \
        .aggregate(year_clients=Count('client')))


    context = {
        'savings_hefei_amount':savings_hefei_amount, 'savings_hefei_client': savings_hefei_client, \
        'loan_hefei_amount':loan_hefei_amount,'loan_hefei_client': loan_hefei_client, \
        'savings_nanyang_amount':savings_nanyang_amount ,'savings_nanyang_client': savings_nanyang_client, \
        'loan_nanyang_amount':loan_nanyang_amount ,'loan_nanyang_client': loan_nanyang_client
        }

    return render(request, 'BankSystem/statistics.html', context)

