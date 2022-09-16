import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from invoiceapp.models import (Address, BankAccountType, CompanyBankDetail, Company, Client, Currency,
                               CompanyAdditionalInfo, Developer, Particular, ResourceType, FixedBidParticular)


def save_address_new_formset(total_forms, data, company=None, client=None, prefix='address'):
    for i in range(total_forms):
        id_address = '{0}-{1}-id'.format(prefix, i)
        if data.get(id_address) == '' or not data.get(id_address):
            zip_code = data.get('{0}-{1}-zip_code'.format(prefix, i), '')
            street = data.get('{0}-{1}-street'.format(prefix, i), '')
            address = data.get('{0}-{1}-address'.format(prefix, i), '')
            try:
                data.pop(id_address)
                data.pop('{0}-{1}-zip_code'.format(prefix, i), '')
                data.pop('{0}-{1}-street'.format(prefix, i), '')
                data.pop('{0}-{1}-address'.format(prefix, i), '')
            except KeyError as e:
                pass

            if company:
                address = Address(address=address, zip_code=zip_code, street=street, company=company)
            else:
                address = Address(address=address, zip_code=zip_code, street=street, client=client)
            address.save()
            data['{0}-TOTAL_FORMS'.format(prefix)] = int(data.get('{0}-TOTAL_FORMS'.format(prefix))) - 1
    return data


def save_bank_formset(total_forms, data, company=None, prefix='form'):
    for i in range(total_forms):
        id_address = '{0}-{1}-id'.format(prefix, i)
        if data.get(id_address) == '' or not data.get(id_address):

            account_number = data.get('{0}-{1}-account_number'.format(prefix, i), '')
            account_type_id = data.get('{0}-{1}-account_type'.format(prefix, i), '')
            ifsc_code = data.get('{0}-{1}-ifsc_code'.format(prefix, i), '')
            bank_ad_code = data.get('{0}-{1}-bank_ad_code'.format(prefix, i), '')
            bank_address = data.get('{0}-{1}-bank_address'.format(prefix, i), '')
            name = data.get('{0}-{1}-name'.format(prefix, i), '')

            try:
                data.pop(id_address)
                data.pop('{0}-{1}-account_number'.format(prefix, i), '')
                data.pop('{0}-{1}-account_type'.format(prefix, i), '')
                data.pop('{0}-{1}-ifsc_code'.format(prefix, i), '')
                data.pop('{0}-{1}-bank_ad_code'.format(prefix, i), '')
                data.pop('{0}-{1}-bank_address'.format(prefix, i), '')
                data.pop('{0}-{1}-name'.format(prefix, i), '')

            except KeyError as e:
                pass

            account_type = "",
            if account_type_id:
                account_type = BankAccountType.objects.get(pk=int(account_type_id))

            bank = CompanyBankDetail(account_number=account_number, account_type=account_type, ifsc_code=ifsc_code,
                                     bank_ad_code=bank_ad_code, company=company, bank_address=bank_address, name=name)

            bank.save()
            data['{0}-TOTAL_FORMS'.format(prefix)] = int(data.get('{0}-TOTAL_FORMS'.format(prefix))) - 1
    return data


def value_exists(value):
    return value if value else ""


def generate_preview_invoice(request):
    company_id = request.GET.get("company")
    client_id = request.GET.get("client")
    company_address_id = request.GET.get("from_address")
    client_address_id = request.GET.get("to_address")
    bank_id = request.GET.get("bank_id")
    invoice = {}

    if company_id:
        company = Company.objects.get(pk=company_id)
        invoice["company_name"] = value_exists(company.name)
        invoice["company_logo_url"] = company.logo.url if company.logo else ""
        invoice["company_website"] = value_exists(company.website)
        invoice["company_phone_number"] = value_exists(company.phone_no)
        invoice["company_email_id"] = value_exists(company.email_id)
        invoice["company_cin"] = value_exists(company.cin)
        company_additional_info = CompanyAdditionalInfo.objects.filter(company=company).first()
        invoice["company_additional"] = "PAN: {0}, <br> IEC: {1}, <br> GSTN: {2}, <br> ".format(
            value_exists(company_additional_info.company_pan_no), value_exists(company_additional_info.iec),
            value_exists(company_additional_info.gstn)
        )
        invoice["company_gstn"] = value_exists(company_additional_info.gstn)
        invoice["company_pan_no"] = value_exists(company_additional_info.company_pan_no)
        invoice["terms_condition"] = "2. {0}".format(value_exists(company_additional_info.terms_condition.strip()))
        invoice["lut_bond"] = value_exists(company_additional_info.lut_bond)
        invoice["self_declaration"] = "Declaration: {0}".format(value_exists(company_additional_info.self_declaration))

    if bank_id:
        company_bank = CompanyBankDetail.objects.get(pk=bank_id)
        invoice["bank_name"] = "{0}".format(value_exists(company_bank.name))
        invoice["bank_address"] = "Address: {0}".format(value_exists(company_bank.bank_address))
        invoice["company_bank"] = "{0}".format(value_exists(company_bank.bank_ad_code))
        invoice["company_bank_acc"] = "Bank A/C No.: {0}".format(value_exists(company_bank.account_number))
        invoice["company_bank_ifsc"] = "IFSC Code: {0}".format(value_exists(company_bank.ifsc_code))
        invoice["bank_ad_code"] = "AD Code: {0}".format(value_exists(company_bank.bank_ad_code))
        invoice["company_bank_eefc"] = "EEFC USD A/C No.: {0}".format(value_exists(company_bank.eefc_account))

    if client_id:
        client = Client.objects.get(pk=client_id)
        invoice["client_name"] = client.name
        invoice["client_logo_url"] = client.logo.url if client.logo else ""
        invoice["client_website"] = value_exists(client.website)
        invoice["project_name"] = client.project.name if client.project else ""

    if company_address_id:
        company_address = Address.objects.get(pk=company_address_id)
        invoice["company_address"] = "{0}, <br>{1}, {2}".format(
            value_exists(company_address.street), value_exists(company_address.address), value_exists(company_address.zip_code)
        )
        invoice["company_zip_code"] = value_exists(company_address.zip_code)

    if client_address_id:
        client_address = Address.objects.get(pk=company_address_id)
        invoice["client_address"] = "{0}, <br>{1}, {2}, <br>".format(
            value_exists(client_address.street), value_exists(client_address.address), value_exists(client_address.zip_code)
        )
        invoice["client_address_zip"] = value_exists(client_address.zip_code)

    return HttpResponse(json.dumps(invoice))


def generate_preview_invoice_temp2(request):
    company_id = request.GET.get("company")
    client_id = request.GET.get("client")
    company_address_id = request.GET.get("from_address")
    client_address_id = request.GET.get("to_address")
    bank_id = request.GET.get("bank_id")
    invoice = {}

    if company_id:
        company = Company.objects.get(pk=company_id)
        invoice["company_name"] = value_exists(company.name)
        invoice["company_logo_url"] = company.logo.url if company.logo else ""
        invoice["company_website"] = value_exists(company.website)
        invoice["company_phone_number"] = value_exists(company.phone_no)
        invoice["company_email_id"] = value_exists(company.email_id)
        invoice["company_cin"] = value_exists(company.cin)
        company_additional_info = CompanyAdditionalInfo.objects.filter(company=company).first()
        invoice["company_additional"] = "PAN: {0}, <br> IEC: {1}, <br> GSTN: {2}, <br> ".format(
            value_exists(company_additional_info.company_pan_no), value_exists(company_additional_info.iec),
            value_exists(company_additional_info.gstn)
        )
        invoice["company_gstn"] = value_exists(company_additional_info.gstn)
        invoice["company_pan_no"] = value_exists(company_additional_info.company_pan_no)
        invoice["terms_condition"] = "2. {0}".format(value_exists(company_additional_info.terms_condition.strip()))
        invoice["lut_bond"] = value_exists(company_additional_info.lut_bond)
        invoice["self_declaration"] = "Declaration: {0}".format(value_exists(company_additional_info.self_declaration))

    if bank_id:
        company_bank = CompanyBankDetail.objects.get(pk=bank_id)
        invoice["bank_name"] = "{0}".format(value_exists(company_bank.name))
        invoice["bank_address"] = "{0}".format(value_exists(company_bank.bank_address))
        invoice["company_bank"] = "{0}".format(value_exists(company_bank.bank_ad_code))
        invoice["company_bank_acc"] = "{0}".format(value_exists(company_bank.account_number))
        invoice["company_bank_ifsc"] = "{0}".format(value_exists(company_bank.ifsc_code))
        invoice["bank_ad_code"] = "{0}".format(value_exists(company_bank.bank_ad_code))
        invoice["company_bank_eefc"] = "{0}".format(value_exists(company_bank.eefc_account))

    if client_id:
        client = Client.objects.get(pk=client_id)
        invoice["client_name"] = client.name
        invoice["client_logo_url"] = client.logo.url if client.logo else ""
        invoice["client_website"] = value_exists(client.website)
        invoice["project_name"] = client.project.name if client.project else ""

    if company_address_id:
        company_address = Address.objects.get(pk=company_address_id)
        invoice["company_address"] = "{0}, {1}, {2}".format(
            value_exists(company_address.street), value_exists(company_address.address), value_exists(company_address.zip_code)
        )
        invoice["company_zip_code"] = value_exists(company_address.zip_code)

    if client_address_id:
        client_address = Address.objects.get(pk=company_address_id)
        invoice["client_address"] = "{0}, {1}, {2}".format(
            value_exists(client_address.street), value_exists(client_address.address), value_exists(client_address.zip_code)
        )
        invoice["client_address_zip"] = value_exists(client_address.zip_code)

    return HttpResponse(json.dumps(invoice))


def save_particular_formset(total_forms, data, invoice=None, prefix='form'):
    for i in range(total_forms):
        id_address = '{0}-{1}-id'.format(prefix, i)
        if data.get(id_address) == '' or not data.get(id_address):

            resource_type = data.get('{0}-{1}-resource_type'.format(prefix, i), '')
            developer = data.get('{0}-{1}-developer'.format(prefix, i), '')
            quantity = data.get('{0}-{1}-quantity'.format(prefix, i), '')
            unit_rate = data.get('{0}-{1}-unit_rate'.format(prefix, i), '')
            amount = data.get('{0}-{1}-amount'.format(prefix, i), '')

            try:
                data.pop(id_address)
                data.pop('{0}-{1}-resource_type'.format(prefix, i), '')
                data.pop('{0}-{1}-developer'.format(prefix, i), '')
                data.pop('{0}-{1}-quantity'.format(prefix, i), '')
                data.pop('{0}-{1}-unit_rate'.format(prefix, i), '')
                data.pop('{0}-{1}-amount'.format(prefix, i), '')

            except KeyError as e:
                pass
            if resource_type:
                resource = ResourceType.objects.get(pk=resource_type)
            else:
                return
            if developer:
                dev = Developer.objects.get(pk=developer)
            else:
                return
            particular = Particular(resource_type=resource, developer=dev, quantity=quantity, unit_rate=unit_rate,
                                    amount=amount, invoice=invoice)

            particular.save()
            data['{0}-TOTAL_FORMS'.format(prefix)] = int(data.get('{0}-TOTAL_FORMS'.format(prefix))) - 1
    return data


def save_fixed_particular_formset(total_forms, data, invoice=None, prefix='fixed_p'):
    for i in range(total_forms):
        id_address = '{0}-{1}-id'.format(prefix, i)
        if data.get(id_address) == '' or not data.get(id_address):

            project_particulars_name = data.get('{0}-{1}-project_particulars_name'.format(prefix, i), '')
            resource_type = data.get('{0}-{1}-resource_type'.format(prefix, i), '')
            developer = data.get('{0}-{1}-developer'.format(prefix, i), '')
            quantity = data.get('{0}-{1}-quantity'.format(prefix, i), '')
            amount = data.get('{0}-{1}-amount'.format(prefix, i), '')

            try:
                data.pop(id_address)                
                data.pop('{0}-{1}-project_particulars_name'.format(prefix, i), '')
                data.pop('{0}-{1}-resource_type'.format(prefix, i), '')
                data.pop('{0}-{1}-developer'.format(prefix, i), '')
                data.pop('{0}-{1}-quantity'.format(prefix, i), '')
                data.pop('{0}-{1}-amount'.format(prefix, i), '')

            except KeyError as e:
                pass

            if resource_type:
                resource = ResourceType.objects.get(pk=resource_type)
            else:
                return
            if developer:
                dev = Developer.objects.get(pk=developer)
            else:
                return
            particular = FixedBidParticular(resource_type=resource, developer=dev, quantity=quantity,
                                            amount=amount, invoice=invoice)

            particular.save()
            data['{0}-TOTAL_FORMS'.format(prefix)] = int(data.get('{0}-TOTAL_FORMS'.format(prefix))) - 1
    return data


def get_sub_unit(request, pk):
    currency = Currency.objects.get(pk=int(pk))
    return HttpResponse(json.dumps({"sub_unit": currency.sub_unit, 'currency_unit': currency.currency_unit}))
