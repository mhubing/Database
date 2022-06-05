from django.contrib import admin

# Register your models here.
from .models import Subbranch, Department, Staff

from .models import Client, Contact
from .models import Account, CheckingAccount, SubbranchClientAccountType, AccessAccount
from .models import Loan, PayLoan, ClientLoan

admin.site.register(Subbranch)
admin.site.register(Department)
admin.site.register(Staff)

admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Account)
admin.site.register(CheckingAccount)
admin.site.register(SubbranchClientAccountType)
admin.site.register(AccessAccount)

admin.site.register(Loan)
admin.site.register(PayLoan)
admin.site.register(ClientLoan)