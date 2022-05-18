from django.contrib import admin

from bank.models import Client, Contact

from bank.models import Subbranch, Department, Staff

# Register your models here.
admin.site.register(Subbranch)

admin.site.register(Department)

admin.site.register(Staff)

admin.site.register(Client)

admin.site.register(Contact)