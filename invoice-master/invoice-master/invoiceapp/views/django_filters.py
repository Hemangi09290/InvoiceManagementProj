import django_filters
from invoiceapp.models import Invoice


class ReportFilter(django_filters.FilterSet):
    OPTIONS = (("Pending", 'Pending'), ("Paid", 'Paid'))
    payment_status = django_filters.ChoiceFilter(empty_label='Select Status', label="Invoice Status",
                                                 choices=OPTIONS)

    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Invoice
        fields = {'payment_status', 'project', 'project_name', 'client', 'created_at'}

    def __init__(self, *args, **kwargs):
        super(ReportFilter, self).__init__(*args, **kwargs)
        self.filters['project'].label = 'Project'
        self.filters['client'].lable = 'Select Client'
        self.filters['created_at'].label = 'Date Range'
        self.form.fields['project'].empty_label = 'Select Project'
        self.form.fields['client'].empty_label = 'Select Client'
