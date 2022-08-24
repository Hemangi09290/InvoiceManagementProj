from django.urls import path
from django.contrib.auth.decorators import login_required
from invoiceapp.views import (InvoiceView, invoice_cancel_view, InvoiceUpdateView, client_cancel_view,
                              CompanyListView, CompanyUpdateView, company_cancel_view, ClientListView, CompanySetup,
                              get_all_addresses, delete_particulars, delete_address, delete_bank, ReportListView,
                              ClientSetup, ClientUpdateView, generate_preview_invoice, InvoiceDetailView,
                              update_payment_status, get_sub_unit)
from invoiceapp.views.common import generate_preview_invoice_temp2

urlpatterns = [
    path('', login_required(CompanyListView.as_view(), login_url='/accounts/login'), name="company-basic"),
    path('company/<pk>/update', login_required(CompanyUpdateView.as_view(), login_url='/accounts/login'),
         name="company-update"),
    path('company/<pk>/cancel', login_required(company_cancel_view, login_url='/accounts/login'),
         name="company-delete"),
    path('company/', login_required(CompanySetup.as_view(), login_url='/accounts/login'), name="company-setup"),

    path('address/<pk>/delete', login_required(delete_address, login_url='/accounts/login'), name="delete-address"),
    path('bank/<pk>/delete', login_required(delete_bank, login_url='/accounts/login'), name="delete-bank"),

    path('clients/', login_required(ClientListView.as_view(), login_url='/accounts/login'), name="client-list"),

    path('client/<pk>/update', login_required(ClientUpdateView.as_view(), login_url='/accounts/login'),
         name="client-update"),
    path('client/<pk>/cancel', login_required(client_cancel_view, login_url='/accounts/login'), name="client-cancel"),

    path('client/', login_required(ClientSetup.as_view(), login_url='/accounts/login'), name="client-setup"),

    path('invoice/', login_required(InvoiceView.as_view(), login_url='/accounts/login'), name="invoice"),
    path('invoices/', login_required(ReportListView, login_url='/accounts/login'), name="invoice-list"),
    path('invoice/<pk>/update', login_required(InvoiceUpdateView.as_view(), login_url='/accounts/login'),
         name="invoice-update"),

    path('invoice/<pk>/cancel', login_required(invoice_cancel_view, login_url='/accounts/login'),name="invoice-cancel"),

   
    path('invoice/<pk>/update-status', login_required(update_payment_status, login_url='/accounts/login'),
         name="invoice-update-status"),


    path('particulars/<pk>/delete', login_required(delete_particulars, login_url='/accounts/login'),
         name="particulars-delete"),
    path('client-address/<pk>', login_required(get_all_addresses, login_url='/accounts/login'), name="client-address"),

    path('invoice-preview/<pk>', login_required(InvoiceDetailView.as_view(), login_url='/accounts/login'),
         name="invoice-preview-fixed"),
    path('invoice-preview/', login_required(generate_preview_invoice, login_url='/accounts/login'),
         name="invoice-preview"),
    path('invoice-preview-temp2/', login_required(generate_preview_invoice_temp2, login_url='/accounts/login'),
         name="invoice-preview-temp2"),
    path('currency/<pk>', login_required(get_sub_unit, login_url='/accounts/login'), name='currency'),
]
