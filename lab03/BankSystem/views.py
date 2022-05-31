from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    
    return HttpResponse("need to finish HtteRequestRediction.")

def clients(request):
    return HttpResponse("need to finish client management.")

def accounts(request):
    return HttpResponse("need to finish account management.")

def loans(request):
    return HttpResponse("need to finish loan management.")

def statistics(request):
    return HttpResponse("need to finish business statistics.")

