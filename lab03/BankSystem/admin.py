from django.contrib import admin

# Register your models here.
from .models import Subbranch, Department, Staff

admin.site.register(Subbranch)
admin.site.register(Department)
admin.site.register(Staff)