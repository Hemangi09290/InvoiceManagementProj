from django import forms
from invoiceapp.models import (Company, CompanyAdditionalInfo,
                               CompanyBankDetail, Client, Invoice, Particular,
                               Address,
                               Currency, FixedBidParticular)
from django.forms import modelformset_factory


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter Company Name *',
                       'class': 'form-control'}),
            'website': forms.TextInput(
                attrs={'placeholder': 'Website ', 'class': 'form-control'}),
            'invoice_initial': forms.TextInput(
                attrs={'placeholder': 'Invoice-Initial',
                       'class': 'form-control', 'required': 'required'}),
            'phone_no': forms.TextInput(
                attrs={'placeholder': 'Phone No.', 'class': 'form-control'}),
            'email_id': forms.EmailInput(
                attrs={'placeholder': 'Email Id', 'class': 'form-control'}),
            'cin': forms.TextInput(
                attrs={'placeholder': 'Enter Cin', 'class': 'form-control'})

        }


class CompanyAdditionalForm(forms.ModelForm):
    class Meta:
        model = CompanyAdditionalInfo
        fields = "__all__"
        exclude = ("company",)
        widgets = {

            'company_pan_no': forms.TextInput(
                attrs={'placeholder': 'Company Pan No ',
                       'class': 'form-control'}),
            'gstn': forms.TextInput(
                attrs={'placeholder': 'Gstn ', 'class': 'form-control'}),
            'iec': forms.TextInput(
                attrs={'placeholder': 'Iec ', 'class': 'form-control'}),

            'lut_bond': forms.TextInput(
                attrs={
                    'placeholder': 'LUT(Legal Under Bond)Information For\
                     Export Product Aand Service ',
                    'class': 'form-control', 'rows': 1, 'cols': 2,
                    'style': 'height: 1em;'}),

            'terms_condition': forms.Textarea(
                attrs={'rows': 1, 'cols': 2,
                       'placeholder': 'Terms And Condtion Ffor Payments ',
                       'class': 'form-control', 'style': 'height: 1em;'}),

            # 'terms_condition': forms.Textarea(
            #    attrs={'rows': 1, 'cols': 2,
            #    'placeholder': 'TERMS AND CONDITION FOR PAYMENTS ',
            #    'class': 'form-control','style': 'height: 1em;'}),

            'self_declaration': forms.Textarea(
                attrs={
                    'placeholder': 'Self Declaration Computer Generated\
                     Invoice and Invoice Information',
                    'cols': 5, 'rows': 4, 'class': 'form-control'}),

        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Client Name *',
                                           'class': 'form-control'}),
            'website': forms.TextInput(
                attrs={'placeholder': 'Website', 'class': 'form-control'}),
            'pan': forms.TextInput(
                attrs={'placeholder': 'Client Pan', 'class': 'form-control'}),
            'gstn': forms.TextInput(
                attrs={'placeholder': 'Gstn', 'class': 'form-control'}),
            'iec': forms.TextInput(
                attrs={'placeholder': 'Iec', 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'agreement_detail': forms.CharField(max_length=200,
                                                widget=forms.TextInput(
                                                    {"placeholder": "Text!",
                                                     'class': 'form-control'})),
            'agreement_date': forms.DateInput(
                attrs={'placeholder': 'Agreement Date',
                       'class': 'form-control date-picker'}),
            'agreement': forms.FileInput(
                attrs={'placeholder': 'Upload Copy Of Agreement',
                       'class': 'form-control',
                       }),
            'phone_no': forms.TextInput(
                attrs={'placeholder': 'Phone No.', 'class': 'form-control'}),
            'email_id': forms.EmailInput(
                attrs={'placeholder': 'Email id', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = 'PROJECT NAME'
        self.fields['project_type'].empty_label = 'PROJECT TYPE'


class CurrencyForm(forms.Form):
    exchange_rate = forms.DecimalField(max_digits=12, decimal_places=2,
                                       required=True, widget=forms.NumberInput(
            attrs={'placeholder': 'Exchange Rate *', 'class': 'form-control'}))
    currency_set = Currency.objects.all()
    currency = forms.ModelChoiceField(
        queryset=currency_set,
        empty_label="currency", required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'placeholder': 'Select Currency',
                   'onchange': "update_currency(this.id, this.value)"})
    )

    class Meta:
        fields = ("currency", "exchange_rate")


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = (
            'created_at', 'from_address_text', 'to_address_text',
            'company_name',
            'client_name', 'project_name',
            'website', "phone_no", "project", "currency_name",
            "currency_symbol",
            "total_amount", "exchange_rate", "company_bank_acc_type_text",
            "company_bank_acc_text",
            "company_bank_add_text", "company_bank_ifsc_text", "bank_ad_code",
            "company_pan_no", "company_iec",
            "company_terms_condition", "company_self_declaration", "bank_name",
            "company_cin", "payment_status"
        )

        widgets = {

            "invoice_number": forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter Invoice Number'}),
            "name_of_person": forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter Name Of Person'}),
            "company": forms.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select Company*',
                       'required': 'required'}),
            "client": forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'Select Client*',
                       'required': 'required'}),
            "from_address": forms.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select Company Address*',
                       'required': 'required'}),
            "to_address": forms.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select Client Address',
                       'required': 'required'}),
            "company_bank": forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'Select Bank',
                       'required': 'required'}),
            "agreement_date": forms.DateInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Select Agreement Date',
                       'required': 'required'}),
            "project_type": forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select project type',
                    'required': 'required',
                    "onchange": "show_hide_particulars_panel(this.id, \
                    this.value)"}
            ),
            "cgst": forms.NumberInput(
                attrs={'class': 'form-control', 'onblur': 'calculate_totals();',
                       'placeholder': 'Enter cgst*', 'required': 'required',
                       'label': 'cgst'}),
            "sgst": forms.NumberInput(
                attrs={'class': 'form-control', 'onblur': 'calculate_totals();',
                       'placeholder': 'Enter sgst*', 'required': 'required',
                       'label': 'sgst'}),
            "igst": forms.NumberInput(
                attrs={'class': 'form-control', 'onblur': 'calculate_totals();',
                       'placeholder': 'Enter igst*', 'required': 'required',
                       'label': 'igst'}),
        }

    def generate_5_digit_integer_with_0(self, value):
        return '{0}{1}'.format((5 - len(str(value))) * '0', str(value))

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['client'].empty_label = 'Select Client'
        self.fields['company'].empty_label = 'Select company'
        self.fields['from_address'].empty_label = 'Select company address'
        self.fields['to_address'].empty_label = 'Select client address'
        self.fields['company_bank'].empty_label = 'Select bank '
        self.fields['invoice_number'].required = False

    def save(self, commit=True, *args, **kwargs):
        invoice = super(InvoiceForm, self).save(commit=False)

        client = self.cleaned_data['client']
        company = self.cleaned_data['company']
        project = client.project
        from_address = self.cleaned_data['from_address']
        company_bank = self.cleaned_data['company_bank']
        to_address = self.cleaned_data['to_address']

        company_additional = CompanyAdditionalInfo.objects.filter(
            company=company).first()
        if from_address:
            from_address_text = "{0}, {1}, {2}".format(from_address.street,
                                                       from_address.address,
                                                       from_address.zip_code
                                                       )
            invoice.from_address_text = from_address_text

        if to_address:
            to_address_text = "{0}, {1}, {2}".format(to_address.street,
                                                     to_address.address,
                                                     to_address.zip_code)
            invoice.to_address_text = to_address_text

        if company_bank:
            invoice.company_bank_acc_type_text = company_bank.account_type. \
                type if company_bank.account_type else ""
            invoice.company_bank_acc_text = company_bank.account_number
            invoice.company_bank_add_text = company_bank.bank_address
            invoice.bank_ad_code = company_bank.bank_ad_code
            invoice.company_bank_ifsc_text = company_bank.ifsc_code
            invoice.bank_name = company_bank.name
            invoice.branch_code = company_bank.branch_code
            invoice.company_eefc = company_bank.eefc_account
        company_invoice_cnt = int(company.invoice_count) + 1
        increment_count = False
        if not invoice.invoice_number:
            increment_count = True
            invoice.invoice_number = "{0}{1}".format(
                company.invoice_initial,
                self.generate_5_digit_integer_with_0(
                    company_invoice_cnt
                )
            )
            company.invoice_count = company_invoice_cnt
            company.save()
        invoice.phone_no = company.phone_no

        invoice.company_cin = company.cin
        # invoice.agreement_date = client.agreement_date
        invoice.project_name = project.name if project else ""
        invoice.website = company.website
        invoice.company_name = company.name
        invoice.client_name = client.name

        if company_additional:
            invoice.company_pan_no = company_additional.company_pan_no
            invoice.company_iec = company_additional.iec
            invoice.company_lut_bond = company_additional.lut_bond
            invoice.company_terms_condition = company_additional.terms_condition
            invoice.company_self_declaration = company_additional. \
                self_declaration

        invoice.exchange_rate = self.cleaned_data["exchange_rate"]
        invoice.currency_name = self.cleaned_data["currency_name"]
        invoice.currency_symbol = self.cleaned_data["currency_symbol"]
        invoice.total_amount = self.cleaned_data["total_amount"]
        invoice.project_type = self.cleaned_data["project_type"]
        invoice.cgst = kwargs.get("cgst")
        invoice.sgst = kwargs.get("sgst")
        invoice.igst = kwargs.get("igst")
        invoice.is_active = True
        invoice.save()
        if increment_count:
            company.invoice_count = company_invoice_cnt
            company.save()
        return invoice


def get_particular_formset(extra_forms=1):
    particulars_formset = modelformset_factory(
        model=Particular,
        exclude=("invoice",),
        widgets={
            "id": forms.HiddenInput(
                attrs={'class': 'form-control input-lg', 'placeholder': 'Id'}),
            "quantity": forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Quantity',
                       'required': 'required'
                       }),
            "unit_rate": forms.NumberInput(attrs={
                'class': 'form-control',
                'onblur': 'calculate_total_amount(this.id, this.value);',
                'placeholder': 'Enter Unit Rate',
                'required': 'required'
            }),
            "resource_type": forms.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select Resource Type',
                       'required': 'required'}),
            "amount": forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Total Amount',
                       'required': 'required',
                       'onblur': 'calculate_amount(this.id, this.value);'})
        }, extra=extra_forms)
    return particulars_formset


def get_address_formset(extra_forms=1, is_company=True):
    address_formset = modelformset_factory(
        model=Address, exclude=("company", "client"),
        widgets={
            "id": forms.HiddenInput(
                attrs={'class': 'form-control input-lg', 'placeholder': 'Id'}),
            "zip_code": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Zip_Code'}),
            "street": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Street'}),
            "address": forms.TextInput(
                attrs={'type': 'address', 'class': 'form-control input-lg',
                       'placeholder': 'Enter Address *',
                       'required': 'required',
                       'oninput': 'get_address(this.id)'}),

        }, extra=extra_forms)

    return address_formset


def get_bank_formset(extra_forms=1):
    bank_formset = modelformset_factory(
        model=CompanyBankDetail, exclude=("company",),

        widgets={
            "account_number": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Account_Number'}),
            "account_type": forms.Select(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Account_Type'}),
            "ifsc_code": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Ifsc_Code',
                       "onblur": "get_ifsc_detail(this.id, this.value)"}),
            "bank_ad_code": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Bank_Ad_Code'}),
            "bank_address": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Bank Address'}),
            "name": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Bank Name '}),
            "branch_code": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Branch Code '}),
            "eefc_account": forms.TextInput(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'EEFC account'}),
            "account_currency": forms.Select(
                attrs={'class': 'form-control input-lg',
                       'placeholder': 'Account currency'}),

        }, extra=extra_forms)
    return bank_formset


def get_fixed_particular_formset(extra_forms=1):
    particulars_formset = modelformset_factory(model=FixedBidParticular,
                                               exclude=("invoice",), widgets={
            "id": forms.HiddenInput(
                attrs={'class': 'form-control input-lg', 'placeholder': 'Id'}),
            "quantity": forms.NumberInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'Quantity',
                    'required': 'required',
                    'onblur': 'calculate_fixed_quantity(this.id, this.value);'
                }),
            "project_particulars_name": forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter project',
                       'required': 'required'}),
            "amount": forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Total Amount',
                       'onblur': 'calculate_fixed_amount(this.id, this.value);',
                       'required': 'required'})
        }, extra=extra_forms)
    return particulars_formset
