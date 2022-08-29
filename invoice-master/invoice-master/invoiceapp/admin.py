from django.contrib import admin

from .models import (Project, Address, Company, CompanyAdditionalInfo, CompanyBankDetail, Client,
                     Invoice, Particular, BankAccountType, ResourceType, Currency, FixedBidParticular, AccountCurency,
                     Developer)


@admin.register(Project)
class ProjectNameAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'company', 'client', 'zip_code', 'street']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['status', 'name', 'logo', 'email_id', 'phone_no', 'website', 'invoice_initial', 'invoice_count',
                    'created_at']


@admin.register(CompanyAdditionalInfo)
class CompanyAdditionalAdmin(admin.ModelAdmin):
    list_display = ['company', 'company_pan_no', 'gstn', 'iec', 'lut_bond', 'terms_condition', 'self_declaration']


@admin.register(CompanyBankDetail)
class CompanyBankDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'account_number', 'account_type', 'ifsc_code', 'bank_ad_code', 'eefc_account',
                    'account_currency']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['status', 'name', 'logo', 'email_id', 'phone_no', 'website', 'pan', 'gstn', 'iec', 'project',
                    'project_type', 'agreement_detail',
                    'agreement_date', 'agreement']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'from_address_text', 'website', 'to_address_text', 'company', 'company_name', 'client',
                    'client_name', 'invoice_number', 'project_name', 'created_at']


@admin.register(Particular)
class ParticularAdmin(admin.ModelAdmin):
    list_display = ["invoice", "resource_type", "quantity", "unit_rate", "amount"]


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ['type']


@admin.register(AccountCurency)
class AccountCurencyAdmin(admin.ModelAdmin):
    list_display = ['cuurency']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'currency', 'currency_unit', 'sub_unit']


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ["resource_type_name"]


@admin.register(FixedBidParticular)
class FixedParticularAdmin(admin.ModelAdmin):
    list_display = ["project_particulars_name", "invoice", "quantity", "amount"]


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_no", "email_id", "project", "project_type", "resource_type"]

