import copy
import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from .common import save_address_new_formset, save_bank_formset
from django.shortcuts import render, redirect, reverse
from invoiceapp.forms import (CompanyForm, CompanyAdditionalForm, get_address_formset, get_bank_formset)
from django.views.generic import FormView, CreateView, ListView

from django.views.generic.edit import UpdateView
from invoiceapp.models import Company, CompanyAdditionalInfo, CompanyBankDetail, Address


class CompanyListView(ListView):
    form = CompanyForm()
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return self.model.objects.filter(status=True)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        companies = context['companies']
        company_address = []
    


        for company in companies:
            comp_additional = CompanyAdditionalInfo.objects.filter(company=company).first()
            addreses = Address.objects.filter(company=company)
            addr = []
            for address in addreses:
                addr.append({
                    "street": address.street,
                    "address": address.address

                })
            company_address.append(
                {
                    "company_name": company.name,
                    "logo": company.logo.url if company.logo else company.logo,
                    "website": company.website,
                    "pan_no": comp_additional.company_pan_no,
                    "iec": comp_additional.iec,
                    "gstn": comp_additional.gstn,
                    "address": addr,
                    "date": company.created_at.date(),
                    "id": company.pk,
                    "email_id": company.email_id,
                    "phone_no": company.phone_no
                }
            )

        context['company_list'] = company_address
        return context



def company_cancel_view(request, pk):
    if request.method == 'POST':
       comp= Company.objects.get(pk=int(pk))
       comp.status=False
       comp.save()
    return HttpResponse(json.dumps({"message": "Stauts Change"}))

def delete_address(request, pk):
    if request.method == 'POST':
        Address.objects.get(pk=pk).delete()
    return HttpResponse(json.dumps({"message": "successfully deleted"}))


def delete_bank(request, pk):
    if request.method == 'POST':
        CompanyBankDetail.objects.get(pk=pk).delete()
    return HttpResponse(json.dumps({"message": "successfully deleted"}))


class CompanySetup(FormView, CreateView):
    address_formset = get_address_formset()
    bank_formset = get_bank_formset()

    def get(self, request, *args, **kwargs):
        form1 = CompanyForm()
        form2 = self.address_formset(queryset=Address.objects.none(), prefix='address')
        form3 = CompanyAdditionalForm()
        form4 = self.bank_formset(queryset=CompanyBankDetail.objects.none())

        return render(request, 'company_setup.html',
                      {'form': form1, 'form2': form2, 'form3': form3, 'form4': form4, "step": 1})

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':

            post_req = copy.deepcopy(request.POST)
            print(post_req)
            if 'logo' in request.FILES:
                form1 = CompanyForm(request.POST, request.FILES)
            else:
                form1 = CompanyForm(request.POST)
            form2 = self.address_formset(post_req, prefix='address')
            form3 = CompanyAdditionalForm(request.POST)
            form4 = self.bank_formset(post_req)

            if form1.is_valid() and form3.is_valid() and form2.is_valid() and form4.is_valid():
                name = form1.cleaned_data['name']
                company = form1.save()

                comp_add = form3.save(commit=False)
                comp_add.company = company
                form3.save()

                for f in form2:
                    add = f.save(commit=False)
                    add.company = company
                    add.save()

                for f in form4:
                    bank = f.save(commit=False)
                    bank.company = company
                    bank.save()
            else:
                return render(request, 'company_setup.html',
                              {'form': form1, 'form2': form2, 'form3': form3, 'form4': form4})
            return redirect(reverse("company-basic"))


class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'company_setup.html'
    form_class = CompanyForm
    address_fmset = get_address_formset(extra_forms=0)
    address_fmset_extra = get_address_formset()
    bank_fmset = get_bank_formset(extra_forms=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = context.get("company")

        context['title'] = 'Update'
        context['logourl'] = company.logo.url if company.logo else company.logo
        context['step'] = int(self.request.GET.get('step', 1))
        address = Address.objects.filter(company=company)

        context["total_items"] = len(address)
        context["is_edit"] = True

        if context["total_items"] == 0:
            address_fmset = get_address_formset(extra_forms=1)
            context["form2"] = address_fmset(queryset=Address.objects.none(), prefix="address")
        else:
            context["form2"] = self.address_fmset(queryset=address, prefix="address")

        bankdetail = CompanyBankDetail.objects.filter(company=company)

        if len(bankdetail) == 0:
            bank_fmset = get_bank_formset(extra_forms=1)
            context["form4"] = bank_fmset(queryset=CompanyBankDetail.objects.none())
        else:
            context["form4"] = self.bank_fmset(queryset=bankdetail)

        aditional_info = CompanyAdditionalInfo.objects.filter(company=company).first()
        form3 = CompanyAdditionalForm(instance=aditional_info)
        if aditional_info:
            context["additional_info_id"] = aditional_info.pk

        context["form3"] = form3
        return context

    def form_valid(self, form):
        company = form.save()

        post_req = copy.deepcopy(self.request.POST)

        form2 = self.address_fmset(post_req, prefix='address')
        post_req = save_address_new_formset(total_forms=len(form2.forms), data=post_req, company=company)
        form2 = self.address_fmset(post_req, prefix='address')
        form3 = CompanyAdditionalForm(self.request.POST)
        form4 = self.bank_fmset(post_req)
        post_req = save_bank_formset(total_forms=len(form4.forms), data=post_req, company=company)
        form4 = self.bank_fmset(post_req)
        if form3.is_valid() and form2.is_valid() and form4.is_valid():

            comp_add = form3.save(commit=False)
            comp_add.pk = post_req.get("additional_info_id")
            comp_add.company = company
            comp_add.save()

            for f in form2:
                add = f.save(commit=False)
                add.company = company
                add.save()

            for f in form4:
                bank = f.save(commit=False)
                bank.company = company
                bank.save()
        else:
            return render(self.request, 'company_setup.html',
                          {'form': form, 'form2': form2, 'form3': form3, 'form4': form4})
        return redirect(reverse("company-basic"))
