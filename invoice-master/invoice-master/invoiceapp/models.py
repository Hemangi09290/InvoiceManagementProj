from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Sum

# Create your models here.

PROJECT_TYPE = (
    ('fixed price', 'Fixed Price'),
    ('hourly', 'Hourly'),
)

ACCOUNT_TYPE = (
    ('inr', 'INR'),
    ('usd', 'USD'),
    ('gbp', 'GBP'),
    ('aud', 'AUD'),
)

PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid')
)


class BankAccountType(models.Model):
    type = models.CharField(max_length=120)

    def __str__(self):
        return self.type


class AccountCurency(models.Model):
    cuurency = models.CharField(max_length=120)

    def __str__(self):
        return self.cuurency


class Currency(models.Model):
    # Enter html code if unable to enter sign in symbol
    symbol = models.CharField(max_length=5, null=True, blank=True)
    currency = models.CharField(max_length=120)
    currency_unit = models.CharField(max_length=120)
    sub_unit = models.CharField(max_length=120)

    def __str__(self):
        return self.currency


class ResourceType(models.Model):
    resource_type_name = models.CharField(max_length=120)

    def __str__(self):
        return self.resource_type_name


# ********************************************

class Company(models.Model):
    status = models.BooleanField(default=True, null=True, blank=True)
    logo = models.ImageField(blank=True, default='company.png',
                             upload_to='logo', null=True)
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    email_id = models.EmailField(max_length=50, null=True, blank=True)
    invoice_initial = models.CharField(max_length=50, default='SYS-INV')
    cin = models.CharField(max_length=50, null=True, blank=True)
    # eefc_account = models.CharField(max_length=30, null=True, blank=True)
    invoice_count = models.IntegerField(default=00000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyAdditionalInfo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True,
                                null=True)
    company_pan_no = models.CharField(max_length=20, blank=True, null=True)
    gstn = models.CharField(max_length=100, blank=True, null=True)
    iec = models.CharField(max_length=100, blank=True, null=True)
    lut_bond = RichTextField(blank=True, null=True)
    terms_condition = RichTextField(blank=True, null=True)
    self_declaration = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.company.name


class CompanyBankDetail(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True,
                                null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_type = models.ForeignKey(BankAccountType, on_delete=models.CASCADE,
                                     blank=True, null=True)
    ifsc_code = models.CharField(max_length=50, blank=True, null=True)
    bank_ad_code = models.CharField(max_length=50, blank=True, null=True)
    bank_address = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    eefc_account = models.CharField(max_length=30, null=True, blank=True)
    account_currency = models.ForeignKey(AccountCurency,
                                         on_delete=models.CASCADE, blank=True,
                                         null=True)

    def __str__(self):
        return "{0}-{1}".format(self.account_number, self.name)


class Project(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Client(models.Model):
    status = models.BooleanField(default=True, null=True, blank=True)
    logo = models.ImageField(blank=True, default='client.png', upload_to='logo',
                             null=True)
    name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    email_id = models.EmailField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=50, blank=True, null=True)
    gstn = models.CharField(max_length=50, blank=True, null=True)
    iec = models.CharField(max_length=50, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True,
                                null=True)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE,
                                    blank=True, null=True)
    agreement_detail = RichTextField(blank=True, null=True)
    agreement_date = models.DateField(blank=True, null=True)
    agreement = models.FileField(upload_to='agreementfile/', blank=True,
                                 null=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,
                                blank=True, default=None,
                                related_name="company")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True,
                               blank=True, default=None, related_name="client")
    address = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    street = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.address


class Invoice(models.Model):
    from_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                     related_name='company_address', null=True,
                                     blank=True)
    from_address_text = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=120, null=True, blank=True)
    to_address_text = models.TextField(null=True, blank=True)
    to_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                   related_name='client_address', null=True,
                                   blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,
                                blank=True)
    company_name = models.CharField(max_length=120)
    company_bank = models.ForeignKey(CompanyBankDetail,
                                     on_delete=models.CASCADE, null=True,
                                     blank=True)
    company_bank_add_text = models.CharField(max_length=300, null=True,
                                             blank=True)
    company_bank_acc_text = models.CharField(max_length=20, null=True,
                                             blank=True)
    company_bank_ifsc_text = models.CharField(max_length=20, null=True,
                                              blank=True)
    company_bank_acc_type_text = models.CharField(max_length=30, null=True,
                                                  blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True,
                               blank=True)
    client_name = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True,
                                blank=True)
    invoice_number = models.CharField(max_length=50)
    project_name = models.CharField(max_length=120, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    agreement_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=2,
                                        default=1)
    total_amount = models.DecimalField(max_digits=13, decimal_places=2)
    currency_name = models.CharField(max_length=32, null=True, blank=True)
    currency_symbol = models.CharField(max_length=10, null=True, blank=True)
    name_of_person = models.CharField(max_length=60, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_ad_code = models.CharField(max_length=20, null=True, blank=True)
    company_pan_no = models.CharField(max_length=15, null=True, blank=True)
    company_iec = models.CharField(max_length=15, null=True, blank=True)
    company_lut_bond = RichTextField(null=True, blank=True)
    company_terms_condition = RichTextField(null=True, blank=True)
    company_self_declaration = RichTextField(null=True, blank=True)
    company_cin = models.CharField(max_length=50, null=True, blank=True)
    company_eefc = models.CharField(max_length=50, null=True, blank=True)
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20,
                                      default="pending")
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE,
                                    default='hourly')
    cgst = models.DecimalField(max_digits=8, decimal_places=2, null=True,
                               blank=True)
    sgst = models.DecimalField(max_digits=8, decimal_places=2, null=True,
                               blank=True)
    igst = models.DecimalField(max_digits=8, decimal_places=2, null=True,
                               blank=True)

    def __str__(self):
        return self.from_address_text if self.from_address_text else self.to_address_text


class Particular(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_rate = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return self.resource_type.resource_type_name

    @classmethod
    def get_sum_of_column(cls, invoice):
        total_hours = cls.objects.filter(invoice=invoice).aggregate(
            Sum("quantity"))
        total_unit_rate = cls.objects.filter(invoice=invoice).aggregate(
            Sum("unit_rate"))
        total_amount = cls.objects.filter(invoice=invoice).aggregate(
            Sum("amount"))
        return (
        total_hours.get("quantity__sum"), total_unit_rate.get("unit_rate__sum"),
        total_amount.get("amount__sum"))


class FixedBidParticular(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    project_particulars_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return self.project_particulars_name

    @classmethod
    def get_sum_of_column(cls, invoice):
        total_hours = cls.objects.filter(invoice=invoice).aggregate(
            Sum("quantity"))
        total_amount = cls.objects.filter(invoice=invoice).aggregate(
            Sum("amount"))
        return total_hours.get("quantity__sum"), total_amount.get("amount__sum")


class Developer(models.Model):
    name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    email_id = models.EmailField(max_length=50, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True,
                                blank=True)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE,
                                    default='hourly')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ParticularDeveloper(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_rate = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    total_amount = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return self.developer.developer_name

    @classmethod
    def get_sum_of_column(cls, invoice):
        total_hours = cls.objects.filter(invoice=invoice).aggregate(
            Sum("quantity"))
        total_unit_rate = cls.objects.filter(invoice=invoice).aggregate(
            Sum("unit_rate"))
        total_amount = cls.objects.filter(invoice=invoice).aggregate(
            Sum("amount"))
        return (
        total_hours.get("quantity__sum"), total_unit_rate.get("unit_rate__sum"),
        total_amount.get("amount__sum"))
