from django.contrib import admin

# Register your models here.
from .models import Subbranch, Department, Staff

from .models import Client, Contact, Account, CheckingAccount, SubbranchClientAccountType

admin.site.register(Subbranch)
admin.site.register(Department)
admin.site.register(Staff)

admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Account)
admin.site.register(CheckingAccount)
admin.site.register(SubbranchClientAccountType)
