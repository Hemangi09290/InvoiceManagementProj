import csv
import time


def create_invoice_csv_file(report_list=None):
    # assign header columns
    filename = str(int(time.time())) + '.csv'
    file = open(filename, 'w', newline='')

    with file:
        headerList = ['Invoice No', 'Company Name', 'Client Name', 'Project Name', 'Bill To',
                      'Particulars', 'Unit Rate', 'Total Amount', 'INR Amount', 'Invoice Date']
        writer = csv.DictWriter(file, fieldnames=headerList)

        # writing data row-wise into the csv file
        writer.writeheader()
        for report in report_list:
            print(report['particulars_unit'])
            # particulars = ','.join(report['particulars_unit']['resource_type'])
            particulars = ''
            # particulars_unit = ','.join(report['particulars_unit']['unit_rate'])
            particulars_unit = ''
            writer.writerow({'Invoice No': report['invoice_number'],
                             'Company Name': report['company_name'],
                             'Client Name': report['client_name'],
                             'Project Name': report['project_name'],
                             'Bill To': report['address'],
                             'Particulars': particulars,
                             'Unit Rate': particulars_unit,
                             'Total Amount': report['inr_price'],
                             'INR Amount': report['inr_price'],
                             'Invoice Date': report['created_at']
                             })
    return filename


def render_to_pdf(template_src, context_dict=None, uri=None):
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from weasyprint.fonts import FontConfiguration
    from weasyprint import HTML

    response = HttpResponse(content_type="application/pdf")

    font = FontConfiguration()
    html = render_to_string(template_src, context_dict)

    HTML(string=html, base_url=uri).write_pdf(response, font_config=font)
    return response
