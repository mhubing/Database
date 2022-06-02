from pydoc import pager
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.clients, name='clients_management'),
    path('add_client', views.add_client),
    path('accounts', views.accounts, name='accounts_management'),
    path('loans', views.loans, name='loans_management'),
    path('statistics', views.statistics, name='business_statistics'),
]