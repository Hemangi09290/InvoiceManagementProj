import datetime
import os
import io
import random
import copy
from zipfile import ZipFile
from django.shortcuts import render, redirect, reverse, HttpResponse

from invoiceapp.models import Client, Address, Invoice, Particular, Project, \
    Company, FixedBidParticular, Currency

from invoiceapp.views.django_filters import ReportFilter
from invoiceapp.utility import create_invoice_csv_file, render_to_pdf
from django.core import serializers

from invoiceapp.utils import convert_to_words


#
# class ReportListView(ListView):
#     model = Invoice
#     template_name = 'report_list.html'
#     context_object_name = 'reports'
#     paginate_by = 10
#
#     def get_report_filter(self, request_data):
#         reports_filter = copy.deepcopy(request_data)
#         project_id = reports_filter.get('project')
#         if project_id:
#             project = Project.objects.get(id=project_id)
#             reports_filter['project_name'] = project.name
#             reports_filter.pop('project')
#         return reports_filter
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         reports_filter = self.get_report_filter(request_data=self.request.GET)
#         self.filterset = ReportFilter(reports_filter, queryset=queryset)
#         return self.filterset.qs.distinct()
#
#     def get_context_data(self, **kwargs):
#         context = super(ReportListView, self).get_context_data(**kwargs)
#
#         reports_filter = self.get_report_filter(request_data=self.request.GET)
#         filtered_cars = ReportFilter(reports_filter, queryset=self.get_queryset())
#         page = self.request.GET.get('page')
#         paginator = Paginator(filtered_cars.qs, self.paginate_by)
#         try:
#             reports = paginator.page(page)
#         except PageNotAnInteger:
#             reports = paginator.page(1)
#         except EmptyPage:
#             reports = paginator.page(paginator.num_pages)
#         reports_list = []
#         for report in reports:
#             reports_list.append(
#                 {
#                     "invoice_number": report.invoice_number,
#                     "company_name": report.company_name,
#                     "client_name": report.client_name,
#                     "project_name": report.project_name,
#                     "id": report.pk,
#                     "address": report.to_address_text,
#                     # "particular": report.particular_set.all(),
#                     # "particulars": serializers.serialize("json", report.particular_set.all()),
#                     "particulars_unit": serializers.serialize('json', report.particular_set.all()),
#                     "created_at": report.created_at,
#                     "inr_price": report.total_amount,
#                     "exchange_rate": report.exchange_rate
#                 }
#             )
#
#         context['reports'] = reports_list
#         if self.request.GET.get('project'):
#             reports_filter['project'] = self.request.GET.get('project')
#             filtered_cars = ReportFilter(reports_filter, queryset=self.get_queryset())
#         context['filter'] = filtered_cars
#         if 'download' in self.request.GET:
#             reports_download_list = []
#             for report in reports:
#
#                 total_hours, total_unit_rate, total_amount = Particular.get_sum_of_column(invoice=report)
#                 context_bottom = {
#                     "total_amount_in_inr": total_amount * report.exchange_rate,
#                     "total_amount": total_amount,
#                     "total_hours": total_hours,
#                     "total_unit_rates": total_unit_rate,
#                     "amount_in_words": convert_to_words(int(total_amount) if total_amount else 0) + "only."
#                 }
#
#                 particulars_ = Particular.objects.filter(invoice=report)
#                 resources, qty, unit_rate, amounts = '', '', '', ''
#                 for particular in particulars_:
#                     resources += str(particular.resource_type.resource_type_name) + "<br>"
#                     qty += str(particular.quantity) + "<br>"
#                     unit_rate += str(particular.unit_rate) + "<br>"
#                     amounts += str(particular.amount) + "<br>"
#                 particulars = {
#                     'resource_types': resources,
#                     'qty': qty,
#                     'amounts': amounts,
#                     'unit_rates': unit_rate
#                 }
#                 reports_download_list.append({
#                     'object': report,
#                     'particulars': particulars,
#                     'context_bottom': context_bottom,
#
#                 })
#             filename = create_invoice_csv_file(reports_list)
#             pdfs = []
#             for report in reports_download_list:
#                 pdf = render_to_pdf('invoice_preview.html', report)
#                 if pdf:
#                     response = HttpResponse(pdf, content_type='application/pdf')
#                     filename = "Invoice_%s.pdf" % ("12341231")
#                     # content = "inline; filename='%s'" % (filename)
#
#                     content = "attachment; filename='%s'" % (filename)
#                     response['Content-Disposition'] = content
#                     return response
#                 return HttpResponse("Not found")
#
#             # content = FileWrapper(filename)
#             # response = HttpResponse(content_type='text/csv')
#             # response['Content-Length'] = os.path.getsize(filename)
#             # response['Content-Disposition'] = 'attachment; filename=%s' % 'invoice.csv'
#             # return response
#         return context


def ReportListView(request):
    model = Invoice
    template_name = 'report_list.html'
    context_object_name = 'reports'
    paginate_by = 10

    reports_filter = copy.deepcopy(request.GET)
    project_id = reports_filter.get('project')
    if project_id:
        project = Project.objects.get(id=project_id)
        reports_filter['project_name'] = project.name
        reports_filter.pop('project')

    # filterset = ReportFilter(reports_filter, queryset=Invoice.objects.all())  filter(status=True)
    filterset = ReportFilter(reports_filter,
                             queryset=Invoice.objects.filter(is_active=True))
    qsa = filterset.qs.distinct()

    reports_list = []
    reports = qsa
    for report in reports:
        reports_list.append(
            {
                "invoice_number": report.invoice_number,
                "company_name": report.company_name,
                "client_name": report.client_name,
                "project_name": report.project_name,
                "project_type": report.project_type,
                "id": report.pk,
                "address": report.to_address_text,
                "particular": report.particular_set.all(),
                # "particulars": serializers.serialize("json", report.particular_set.all()),
                "particulars_unit": serializers.serialize('json',
                                                          report.particular_set.all()),
                "created_at": report.created_at,
                "inr_price": report.total_amount,
                "exchange_rate": report.exchange_rate,
                "payment_status": report.payment_status
            }
        )

    filtered_cars = filterset
    if 'download' in request.GET:
        reports_download_list = []
        for report in reports:
            invoice = Invoice.objects.get(pk=report.id)
            currency_qs = Currency.objects.filter(
                currency=invoice.currency_name, symbol=invoice.currency_symbol
            ).first()

            cgst_amount, sgst_amount, igst_amount = 0, 0, 0
            resources, qty, unit_rate, amounts = '', '', '', ''
            developers = ''
            if report.project_type == 'hourly':
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
                    amount_in_words = "{0} {1}".format(x,
                                                       currency_qs.currency_unit)
                    if int(amt_post):
                        y = convert_to_words(int(amt_post) if amt_post else 0)
                        amount_in_words = "{0} and {1} {2}".format(
                            amount_in_words, y, currency_qs.sub_unit)

                context_bottom = {
                    "total_amount_in_inr": round(
                        total_amount * report.exchange_rate, 2),
                    "total_amount": round(total_amount, 2),
                    "total_hours": total_hours,
                    "total_unit_rates": round(total_unit_rate, 2),
                    "amount_in_words": amount_in_words + " only."
                }

                particulars = Particular.objects.filter(invoice=invoice)

                for particular in particulars:
                    resources += str(
                        particular.resource_type.resource_type_name) + "<br>"
                    developers += str(
                        particular.developer.name) + "<br>"
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
                        2),
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
                    amount_in_words = "{0} {1}".format(x,
                                                       currency_qs.currency_unit)
                    if int(amt_post):
                        y = convert_to_words(int(amt_post) if amt_post else 0)
                        amount_in_words = "{0} and {1} {2}".format(
                            amount_in_words, y, currency_qs.sub_unit)
                context_bottom = {
                    "total_amount_in_inr": round(
                        total_amount * report.exchange_rate, 2),
                    "total_amount": round(total_amount, 2),
                    "total_hours": total_hours,
                    "total_unit_rates": "-",
                    "amount_in_words": amount_in_words + " only."
                }
                particulars = FixedBidParticular.objects.filter(invoice=invoice)

                for particular in particulars:
                    resources += str(
                        particular.resource_type.resource_type_name) + "<br>"
                    developers += str(
                        particular.developer.name) + "<br>"
                    qty += str(particular.quantity) + "<br>"
                    amounts += str(particular.amount) + "<br>"

            if invoice.currency_name == 'INR':

                if invoice.cgst:
                    resources += "CGST " + str(invoice.cgst).replace(
                        '.00', '') + "%<br>"
                    amounts += str(cgst_amount) + "<br>"
                if invoice.sgst:
                    resources += "SGST " + str(invoice.sgst).replace(
                        '.00', '') + "%<br>"
                    amounts += str(sgst_amount) + "<br>"
                if invoice.igst:
                    resources += "IGST " + str(invoice.igst).replace(
                        '.00', '') + "%<br>"
                    amounts += str(igst_amount) + "<br>"

            particulars = {
                'resource_types': resources,
                'developers': developers,
                'qty': qty,
                'amounts': amounts,
                'unit_rates': unit_rate
            }
            reports_download_list.append({
                'object': report,
                'particulars': particulars,
                'context_bottom': context_bottom,

            })
        byte_stream = io.BytesIO()
        zf = ZipFile(byte_stream, "w")
        zip_filename = "Invoice-{0}.zip".format(
            datetime.datetime.now().strftime("%Y-%m-%d"))

        for report in reports_download_list:

            # pdf = render_to_pdf('invoice_preview.html', report, uri=request.get_host())
            pdf = render_to_pdf('invoice_preview.html', report,
                                uri=request.get_host())
            if pdf:
                zip_path = os.path.join(
                    "{0}.pdf".format(report.get('object').invoice_number))
                zf.writestr(zip_path, pdf.content)

        zf.close()
        if reports_download_list:
            response = HttpResponse(byte_stream.getvalue(),
                                    content_type="application/x-zip-compressed")
            response[
                'Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return response

    return render(request, 'report_list.html',
                  context={'reports': reports_list, 'filter': filtered_cars})
