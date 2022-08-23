import copy
import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from invoiceapp.models import Client, Address, Company, CompanyBankDetail
from invoiceapp.forms import ClientForm, get_address_formset
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import CreateView, ListView, FormView

from .common import save_address_new_formset


class ClientListView(ListView):
    form = ClientForm()
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return self.model.objects.filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        clients = context['clients']
        client_list = []

        for client in clients:
            addreses = Address.objects.filter(client=client)
            addr = []
            for address in addreses:
                addr.append({
                    "street": address.street,
                    "zip_code": address.zip_code,
                    "address": address.address
                    # "country": address.country,
                    # "phone_no": address.phone_no,
                    # "city": address.city,
                    # "email": address.email_id
                })

            client_list.append(
                {
                    "logo": client.logo.url if client.logo else client.logo,
                    "client_name": client.name,
                    "website": client.website,
                    "id": client.pk,
                    "date": client.agreement_date,
                    "project": client.project.name if client.project else "",
                    "project_type": client.project_type,
                    "address": addr
                }
            )

        context['client_lists'] = client_list
        return context


def client_cancel_view(request, pk):
    if request.method == 'POST':
        client = Client.objects.get(pk=int(pk))
        client.status = False
        client.save()
    return HttpResponse(json.dumps({"message": "Stauts Change"}))


def get_all_addresses(request, pk):
    address = []
    company_banks = []
    company_banks_dict = {}
    address_required = {}
    result = {}
    agreement_date = ""
    project_type = "hourly"
    if request.method == 'GET':
        type_ = request.GET.get('type')
        if type_.lower() == 'client':
            objs = Client.objects.get(pk=pk)
            project_type = objs.project_type
            address = Address.objects.filter(client=objs)
            agreement_date = objs.agreement_date.strftime('%Y-%m-%d') if objs.agreement_date else ""
        else:
            objs = Company.objects.get(pk=pk)
            address = Address.objects.filter(company=objs)
            company_banks = CompanyBankDetail.objects.filter(company=objs)

    for add in address:
        address_required.update({add.pk: add.street})

    for bank in company_banks:
        company_banks_dict.update({bank.pk: "{0} - {1}".format(bank.account_number, bank.company.name)})

    result.update({"address": address_required})
    if company_banks_dict:
        result.update({"bank": company_banks_dict})
        return HttpResponse(json.dumps(result))
    result.update({"agreement_date": agreement_date})
    result.update({"project_type": project_type})
    print(result)
    return HttpResponse(json.dumps(result))


class ClientSetup(FormView, CreateView):
    address_formset = get_address_formset(is_company=False)

    def get(self, request, *args, **kwargs):
        form1 = ClientForm()
        form2 = self.address_formset(queryset=Address.objects.none(), prefix='address')
        return render(request, 'client_setup.html',
                      {'form': form1, 'form2': form2, "step": 1})

    def post(self, request, *args, **kwargs):
        print('***** Inside post **********')
        if request.method == 'POST':
            print('***** Inside post **********')

            post_req = copy.deepcopy(request.POST)
            # print(post_req)

            if 'logo' in request.FILES or 'agreement' in request.FILES:
                form1 = ClientForm(request.POST, request.FILES)
            else:
                form1 = ClientForm(request.POST)
            form2 = self.address_formset(post_req, prefix='address')
            # form2 = self.address_formset(post_req,)

            if form1.is_valid() and form2.is_valid():
                client = form1.save()

                for f in form2:
                    client_add = f.save(commit=False)
                    client_add.client = client
                    client_add.save()
            else:
                return render(request, 'client_setup.html', {'form': form1, 'form2': form2})
        return redirect(reverse("client-list"))


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'client_setup.html'
    form_class = ClientForm
    address_fmset = get_address_formset(extra_forms=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = context.get("client")
        context['title'] = 'Update'
        context['logourl'] = client.logo.url if client.logo else ""
        context['agreement'] = client.agreement.url if client.agreement else ""
        context['step'] = int(self.request.GET.get('step', 1))
        address = Address.objects.filter(client=client)

        context["total_items"] = len(address)
        if context["total_items"] == 0:
            address_fmset = get_address_formset(extra_forms=1)
            context["form2"] = address_fmset(queryset=Address.objects.none(), prefix="address")
        else:
            context["form2"] = self.address_fmset(queryset=address, prefix="address")
        context["is_edit"] = True
        return context

    def form_valid(self, form):

        client = form.save()
        post_req = copy.deepcopy(self.request.POST)
        form2 = self.address_fmset(post_req, prefix='address')
        post_req = save_address_new_formset(total_forms=len(form2.forms), data=post_req, client=client)
        form2 = self.address_fmset(post_req, prefix='address')

        for i in range(len(form2.forms)):
            id_address = 'address-{0}-id'.format(i)
            if not post_req.get(id_address):
                post_req[id_address] = ''

        if form2.is_valid():
            for f in form2:
                add = f.save(commit=False)
                add.client = client
                add.save()
        else:
            return render(self.request, 'client_setup.html', {'form': form, 'form2': form2})
        return redirect(reverse("client-list"))
