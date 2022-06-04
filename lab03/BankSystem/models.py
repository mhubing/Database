from asyncio import constants
from datetime import date
from locale import currency
from operator import mod
# from tkinter import CASCADE
from django.db import models
from django.forms import CharField, DecimalField
from pymysql import NULL


# Create your models here.


# 1.支行表 Subbranch
class Subbranch(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=64)
    asset = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "Subbranch"

# 2.部门表 Department
class Department(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=30, blank=True)
    subbranch_name = models.ForeignKey(Subbranch, on_delete=models.CASCADE, verbose_name="subbranch_name")
    leader_id = models.ForeignKey('Staff', on_delete=models.CASCADE, blank=True, null=True, verbose_name="leader_id")

    class Meta:
        db_table = "Department"


# 3.员工表 Staff
class Staff(models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="department_id")
    hire_date = models.DateField(default=date.today, editable=True)

    class Meta:
        db_table = "Staff"


# 4.客户表 Client
class Client(models.Model):
    id = models.CharField(max_length=18, primary_key=True, )
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=22, unique=True)
    address = models.CharField(max_length=100)
    staff_id = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="staff_id")
    staff_type_choices = [
        ('account_principal', 'account principal'),
        ('loan_principal', 'loan principal'),
    ]
    staff_type = models.CharField(max_length=20, choices=staff_type_choices, null=True, blank=True)

    class Meta:
        db_table = "Client"


# 5.联系人表 Contact
class Contact(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client_id")
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=22, unique=True)
    email = models.EmailField(unique=True)
    relation = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client_id', 'name'], name='Contact Primary key')
        ]
        db_table = "Contact"


# 6.账户表 Account
class Account(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    balanch = models.DecimalField(max_digits=20, decimal_places=2)
    open_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Account"


# 7.储蓄账户表 SavingsAccount
class SavingsAccount(models.Model):
    account_id = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, verbose_name="account_id")
    interest_rate = models.DecimalField
    currency_type = models.CharField(max_length=20)

    class Meta:
        db_table = "SavingsAccount"


# 8.支票账户表 CheckingAccount
class CheckingAccount(models.Model):
    account_id = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, verbose_name="account_id")
    overdraft = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "CheckingAccount"


# 9.访问账户表 AccessAccount
class AccessAccount(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="account_id")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client_id")
    least_recently_access = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account_id', 'client_id'], name='AccessAccount Primary key')
        ]
        db_table = "AccessAccount"


# 10.贷款表 Loan
class Loan(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    subbranch_name = models.ForeignKey(Subbranch, on_delete=models.CASCADE, verbose_name="subbranch_name")
    loan_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    loan_status_choices = [
        ('issuing', 'issuing'),
        ('issued', 'issued'),
    ]
    loan_status = models.CharField(max_length=20, choices=loan_status_choices, default='issued')

    class Meta:
        db_table = "Loan"


# 11.支付贷款表 PayLoan
class PayLoan(models.Model):
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, verbose_name="loan_id")
    pay_date = models.DateTimeField(auto_now_add=True)
    pay_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['loan_id', 'pay_date'], name='PayLoan Primary Key')
        ]
        db_table = "PayLoan"


# 12.客户_贷款表 ClientLoan
class ClientLoan(models.Model):
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, verbose_name="loan_id")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client_id")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['loan_id', 'client_id'], name='ClientLoan Primary Key')
        ]
        db_table = "ClientLoan"


# 13.支行-客户-账户类型表 SubbranchClientAccountType
class SubbranchClientAccountType(models.Model):
    subbranch_name = models.ForeignKey(Subbranch, on_delete=models.CASCADE, verbose_name="subbranch_name")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client_id")
    account_type_choices = [
        ('saving_account', 'saving_account'),
        ('loan_principal', 'loan principal'),
    ]
    account_type = models.CharField(max_length=20, choices=account_type_choices, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subbranch_name', 'client_id', 'account_type'], name='SCAT Primary key')
        ]
        db_table = "SubbranchClientAccountType"