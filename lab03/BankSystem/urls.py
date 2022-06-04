from pydoc import pager
from django.urls import path

from . import views

app_name = 'BankSystem'
urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.clients, name='clients_management'),
    path('clients/add_client', views.add_client, name='add_client'),
    path('clients/edit_client/<client_id>', views.edit_client, name="edit_client"),
    path('clients/del_client/<client_id>', views.del_client, name="delete_client"),
    # path('clients/contacts', views.view_contacts, name="view_contacts"),
    path('clients/contacts/<client_id>', views.contacts, name="contacts"),
    path('clients/add_contact/<client_id>', views.add_contact, name="add_contact"),
    path('clients/del_contact/<client_id>/<contact_name>', views.del_contact, name="del_contact"),
    path('clients/edit_contact/<client_id>/<contact_name>', views.edit_contact, name="edit_contact"),
    path('accounts', views.accounts, name='accounts_management'),
    path('accounts/add_checking', views.add_checking, name="add_checking"),
    path('accounts/add_savings', views.add_savings, name="add_savings"),
    path('loans', views.loans, name='loans_management'),
    path('statistics', views.statistics, name='business_statistics'),
]