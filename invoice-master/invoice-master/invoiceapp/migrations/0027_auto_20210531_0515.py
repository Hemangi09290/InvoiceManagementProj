# Generated by Django 3.1.3 on 2021-05-31 05:15

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoiceapp', '0026_auto_20210323_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='agreement',
            field=models.FileField(blank=True, null=True, upload_to='agreementfile/'),
        ),
        migrations.AlterField(
            model_name='client',
            name='agreement_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='agreement_detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='gstn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='iec',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='pan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.project'),
        ),
        migrations.AlterField(
            model_name='client',
            name='project_type',
            field=models.CharField(blank=True, choices=[('fixed bid', 'Fixed Bid'), ('hourly', 'Hourly')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='company_pan_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='gstn',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='iec',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='lut_bond',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='self_declaration',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companyadditionalinfo',
            name='terms_condition',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companybankdetail',
            name='account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='companybankdetail',
            name='bank_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='companybankdetail',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]