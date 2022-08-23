import copy
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import FormView, CreateView, DetailView
from invoiceapp.models import Invoice, Particular, Currency, Company, \
    FixedBidParticular
from invoiceapp.forms import InvoiceForm, get_particular_formset, CurrencyForm, \
    get_fixed_particular_formset

from invoiceapp.utils import convert_to_words
from .common import save_particular_formset, save_fixed_particular_formset


class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoice.html'
    form_class = InvoiceForm
    particulars_fmset = get_particular_formset(extra_forms=0)
    fixed_particular_formset = get_fixed_particular_formset(extra_forms=0)

    particulars_formset_extra = get_particular_formset(extra_forms=1)
    fixed_particular_formset_extra = get_fixed_particular_formset(extra_forms=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = context.get("invoice")
        currency_qs = Currency.objects.filter(
            currency=invoice.currency_name, symbol=invoice.currency_symbol
        ).first()
        context['title'] = 'Update'
        context['step'] = int(self.request.GET.get('step', 1))
        if invoice.project_type == 'hourly':
            total_hours, total_unit_rate, total_amount = Particular.get_sum_of_column(
                invoice=invoice)
            total_amount = round(total_amount, 2) if total_amount else 0

            if invoice.currency_name == 'INR':
                cgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.cgst if invoice.cgst else 0) / 100,
                    2)
                sgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.sgst if invoice.sgst else 0) / 100,
                    2)

                igst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.igst if invoice.igst else 0) / 100,
                    2)
                total_amount = total_amount + cgst_amount + sgst_amount + \
                               igst_amount

            split_amt = str(total_amount).split('.')

            amount_in_words = 'zero'
            if '.' in str(total_amount):
                amt_pre = split_amt[0]
                amt_post = split_amt[1]

                x = convert_to_words(int(amt_pre) if amt_pre else 0)
                amount_in_words = "{0} {1}".format(x, currency_qs.currency_unit)
                if int(amt_post):
                    y = convert_to_words(int(amt_post) if amt_post else 0)
                    amount_in_words = "{0} and {1} {2}".format(amount_in_words,
                                                               y,
                                                               currency_qs.sub_unit)
            context_bottom = {
                "total_amount": round(total_amount, 2),
                "total_hours": total_hours,
                "total_unit_rates": round(total_unit_rate, 2),
                "amount_in_words": amount_in_words + " only.",
                "fixed_total_amount": 0,
                "fixed_total_hours": 0,
                "fixed_amount_in_words": "zero only"
            }
            particulars = Particular.objects.filter(invoice=invoice)
            context["total_items"] = len(particulars)
            context["pform"] = self.particulars_fmset(queryset=particulars)
            context["fixed_p_form"] = self.fixed_particular_formset_extra(
                queryset=FixedBidParticular.objects.none(),
                prefix='fixed_p')

        else:
            total_hours, total_amount = FixedBidParticular.get_sum_of_column(
                invoice=invoice)
            total_amount = round(total_amount, 2) if total_amount else 0

            if invoice.currency_name == 'INR':
                cgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.cgst if invoice.cgst else 0) / 100,
                    2)
                sgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.sgst if invoice.sgst else 0) / 100,
                    2)
                igst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.igst if invoice.igst else 0) / 100,
                    2)
                total_amount = total_amount + cgst_amount + sgst_amount + \
                               igst_amount

            split_amt = str(total_amount).split('.')
            amount_in_words = 'zero'
            if '.' in str(total_amount):
                amt_pre = split_amt[0]
                amt_post = split_amt[1]
                x = convert_to_words(int(amt_pre) if amt_pre else 0)
                amount_in_words = "{0} {1}".format(x, currency_qs.currency_unit)
                if int(amt_post):
                    y = convert_to_words(int(amt_post) if amt_post else 0)
                    amount_in_words = "{0} and {1} {2}".format(amount_in_words,
                                                               y,
                                                               currency_qs.sub_unit)
            context_bottom = {
                "total_amount": 0,
                "total_hours": 0,
                "amount_in_words": "zero only.",
                "total_unit_rates": 0,
                "fixed_total_amount": round(total_amount, 2),
                "fixed_total_hours": total_hours,
                "fixed_amount_in_words": amount_in_words + " only."
            }
            fixed_particulars = FixedBidParticular.objects.filter(
                invoice=invoice)
            context["total_items"] = len(fixed_particulars)
            context["fixed_p_form"] = self.fixed_particular_formset(
                queryset=fixed_particulars, prefix='fixed_p')
            context["pform"] = self.particulars_formset_extra(
                queryset=Particular.objects.none())
        context["is_edit"] = True

        currency_form = CurrencyForm(initial={'currency': currency_qs,
                                              'exchange_rate': invoice.exchange_rate}, )
        context["currency_form"] = currency_form
        context["currency_name"] = invoice.currency_name
        context["currency_sub_unit"] = currency_qs.sub_unit
        context["currency_unit"] = currency_qs.currency_unit
        context["context"] = context_bottom
        return context

    def form_valid(self, form):
        post_req = copy.deepcopy(self.request.POST)
        if post_req.get("project_type") != 'hourly':
            cgst = post_req.get("fixed_cgst")
            sgst = post_req.get("fixed_sgst")
            igst = post_req.get("fixed_igst")
        else:
            cgst = post_req.get("cgst")
            sgst = post_req.get("sgst")
            igst = post_req.get("igst")

        currency_form = CurrencyForm(self.request.POST)
        if currency_form.is_valid():
            currency = currency_form.cleaned_data["currency"]
            form.cleaned_data["exchange_rate"] = currency_form.cleaned_data[
                "exchange_rate"]
            form.cleaned_data["currency_name"] = currency.currency
            form.cleaned_data["currency_symbol"] = currency.symbol
            form.cleaned_data["total_amount"] = self.request.POST.get(
                "total_amount")
        invoice = form.save(cgst=cgst, sgst=sgst, igst=igst)

        if post_req.get("project_type") == 'hourly':
            p_form = self.particulars_fmset(post_req)
            post_req = save_particular_formset(total_forms=len(p_form.forms),
                                               data=post_req, invoice=invoice)
            p_form = self.particulars_fmset(post_req)
        else:
            p_form = self.fixed_particular_formset(post_req, prefix='fixed_p')
            post_req = save_fixed_particular_formset(
                total_forms=len(p_form.forms), data=post_req, invoice=invoice)
            p_form = self.fixed_particular_formset(post_req, prefix='fixed_p')
        if p_form.is_valid():
            for f in p_form:
                attribute = f.save(commit=False)
                attribute.invoice = invoice
                attribute.save()

        return redirect(reverse("invoice-list"))


class InvoiceView(FormView, CreateView):
    particulars_formset = get_particular_formset(extra_forms=1)
    fixed_particular_formset = get_fixed_particular_formset(extra_forms=1)

    def get(self, request, *args, **kwargs):
        form = InvoiceForm()
        pform = self.particulars_formset(queryset=Particular.objects.none())
        fixed_p_form = self.fixed_particular_formset(
            queryset=FixedBidParticular.objects.none(), prefix='fixed_p')
        context = {
            "total_amount": 0,
            "total_hours": 0,
            "total_unit_rates": 0,
            "amount_in_words": "zero only"
        }
        companies = Company.objects.all()
        sys_company = Company.objects.filter(name='systango').first()
        selected_companies = sys_company if sys_company else Company.objects.first()
        currency_form = CurrencyForm()
        return render(request, 'invoice.html', {'form': form, "pform": pform,
                                                'fixed_p_form': fixed_p_form,
                                                "currency_form": currency_form,
                                                "context": context,
                                                "companies": companies,
                                                "selected_companies": selected_companies})

    def post(self, request, *args, **kwargs):

        post_req = copy.deepcopy(request.POST)
        project_type = post_req.get("project_type")
        if project_type == 'hourly':
            cgst = post_req.get("cgst")
            sgst = post_req.get("sgst")
            igst = post_req.get("igst")
            resource_type_values = post_req.getlist("form-0-resource_type")

            idx = 0
            for value in resource_type_values:
                post_req["form-{0}-resource_type".format(idx)] = value
                idx += 1
            pform = self.particulars_formset(post_req)
        else:
            cgst = post_req.get("fixed_cgst")
            sgst = post_req.get("fixed_sgst")
            igst = post_req.get("fixed_igst")

            fixed_type_values = post_req.getlist(
                "fixed_p-0-project_particulars_name")
            idx = 0
            for value in fixed_type_values:
                post_req["fixed_p-{0}-project_particulars_name".format(
                    idx)] = value
                idx += 1
            pform = self.fixed_particular_formset(post_req,
                                                  prefix='fixed_p')
        form = InvoiceForm(post_req)

        currency_form = CurrencyForm(post_req)

        if form.is_valid() and pform.is_valid() and currency_form.is_valid():

            currency = currency_form.cleaned_data["currency"]
            form.cleaned_data["exchange_rate"] = currency_form.cleaned_data[
                "exchange_rate"]
            form.cleaned_data["currency_name"] = currency.currency
            form.cleaned_data["currency_symbol"] = currency.symbol
            form.cleaned_data["total_amount"] = post_req.get("total_amount")
            invoice = form.save(cgst=cgst, sgst=sgst, igst=igst)

            for f in pform:
                attribute = f.save(commit=False)
                attribute.invoice = invoice
                attribute.save()

            return redirect(reverse("invoice-list"))

        return render(request, 'invoice.html', {"step": 1})


def invoice_cancel_view(request, pk):
    if request.method == 'POST':
        invoice = Invoice.objects.get(pk=int(pk))
        invoice.is_active = False
        invoice.save()
    return redirect(reverse("invoice-list"))


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice_preview.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)

        # add extra field
        invoice = self.get_object()
        resources, qty, unit_rate, amounts = '', '', '', ''
        currency_qs = Currency.objects.filter(
            currency=invoice.currency_name, symbol=invoice.currency_symbol
        ).first()
        cgst_amount, sgst_amount, igst_amount = 0, 0, 0

        if invoice.project_type == 'hourly':
            total_hours, total_unit_rate, total_amount = Particular.get_sum_of_column(
                invoice=invoice)

            total_amount = round(total_amount, 2) if total_amount else 0
            split_amt = str(total_amount).split('.')

            if invoice.currency_name == 'INR':
                cgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.cgst if invoice.cgst else 0) / 100,
                    2)
                sgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.sgst if invoice.sgst else 0) / 100,
                    2)
                igst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.igst if invoice.igst else 0) / 100,
                    2)
                total_amount = total_amount + cgst_amount + sgst_amount + \
                               igst_amount

            amount_in_words = 'zero'
            if '.' in str(total_amount):
                amt_pre = split_amt[0]
                amt_post = split_amt[1]
                x = convert_to_words(int(amt_pre) if amt_pre else 0)
                amount_in_words = "{0} {1}".format(x, currency_qs.currency_unit)

                if int(amt_post):
                    y = convert_to_words(int(amt_post) if amt_post else 0)
                    amount_in_words = "{0} and {1} {2}".format(amount_in_words,
                                                               y,
                                                               currency_qs.sub_unit)

            context_bottom = {
                "total_amount_in_inr": round(
                    total_amount * invoice.exchange_rate, 2),
                "total_amount": round(total_amount, 2),
                "total_hours": total_hours,
                "total_unit_rates": round(total_unit_rate, 2),
                "amount_in_words": amount_in_words + " only."
            }

            particulars = Particular.objects.filter(invoice=invoice)

            for particular in particulars:
                resources += str(
                    particular.resource_type.resource_type_name) + "<br>"
                qty += str(particular.quantity) + "<br>"
                unit_rate += str(particular.unit_rate) + "<br>"
                amounts += str(particular.amount) + "<br>"

        else:
            total_hours, total_amount = FixedBidParticular.get_sum_of_column(
                invoice=invoice)
            total_amount = round(total_amount, 2) if total_amount else 0
            split_amt = str(total_amount).split('.')

            if invoice.currency_name == 'INR':
                cgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.cgst if invoice.cgst else 0) / 100,
                    2)
                sgst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.sgst if invoice.sgst else 0) / 100,
                    2)
                igst_amount = round(
                    (total_amount if total_amount else 0) * (
                        invoice.igst if invoice.igst else 0) / 100,
                    2)
                total_amount = total_amount + cgst_amount + sgst_amount + \
                               igst_amount

            amount_in_words = 'zero'
            if '.' in str(total_amount):
                amt_pre = split_amt[0]
                amt_post = split_amt[1]
                x = convert_to_words(int(amt_pre) if amt_pre else 0)
                amount_in_words = "{0} {1}".format(x, currency_qs.currency_unit)
                if int(amt_post):
                    y = convert_to_words(int(amt_post) if amt_post else 0)
                    amount_in_words = "{0} and {1} {2}".format(amount_in_words,
                                                               y,
                                                               currency_qs.sub_unit)

            context_bottom = {
                "total_amount_in_inr": round(
                    total_amount * invoice.exchange_rate, 2),
                "total_amount": round(total_amount, 2),
                "total_hours": total_hours,
                "total_unit_rates": "-",
                "amount_in_words": amount_in_words + " only."
            }

            particulars = FixedBidParticular.objects.filter(invoice=invoice)

            for particular in particulars:
                resources += str(particular.project_particulars_name) + "<br>"
                qty += str(particular.quantity) + "<br>"
                amounts += str(particular.amount) + "<br>"
        context["context_bottom"] = context_bottom

        if invoice.currency_name == 'INR':
            if invoice.cgst:
                resources += "CGST " + str(invoice.cgst).replace('.00', '') + "%<br>"
                amounts += str(cgst_amount) + "<br>"
            if invoice.sgst:
                resources += "SGST " + str(invoice.sgst).replace('.00', '') + "%<br>"
                amounts += str(sgst_amount) + "<br>"
            if invoice.igst:
                resources += "IGST " + str(invoice.igst).replace('.00', '') + "%<br>"
                amounts += str(igst_amount) + "<br>"

        context['particulars'] = {
            'resource_types': resources,
            'qty': qty,
            'amounts': amounts,
            'unit_rates': unit_rate
        }
        context["is_preview"] = True
        return context


def update_payment_status(request, pk):
    reverse_status_value = {
        "paid": "Pending",
        "pending": "Paid"
    }
    payment_status = request.POST.get("payment_status")
    if payment_status and payment_status.lower() in ["paid", "pending"]:
        invoice = Invoice.objects.get(pk=pk)
        invoice.payment_status = reverse_status_value.get(
            payment_status.lower())
        invoice.save()
        return HttpResponse(
            json.dumps({"message": "Payment status updated", "success": True}),
            status=200)

    else:
        return HttpResponse(json.dumps(
            {"message": "Invalid status selection", "success": False}),
                            status=400)
