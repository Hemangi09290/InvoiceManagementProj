# Generated by Django 3.1.7 on 2021-03-01 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, upload_to='logo')),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.country')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyBankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20)),
                ('account_type', models.CharField(choices=[('inr', 'INR'), ('usd', 'USD'), ('gbp', 'GBP'), ('aud', 'AUD')], default='INR', max_length=6)),
                ('ifsc_code', models.CharField(max_length=50)),
                ('bank_ad_code', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyAdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_pan_no', models.CharField(max_length=20)),
                ('gstn', models.CharField(max_length=100)),
                ('iec', models.CharField(max_length=100)),
                ('lut_bond', models.TextField()),
                ('terms_condition', models.TextField()),
                ('self_declaration', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, upload_to='logo')),
                ('name', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=50)),
                ('pan', models.CharField(max_length=50)),
                ('gstn', models.CharField(max_length=50)),
                ('iec', models.CharField(max_length=50)),
                ('project_type', models.CharField(choices=[('fixed bid', 'Fixed Bid'), ('hourly', 'Hourly')], max_length=50)),
                ('agreement_detail', models.TextField()),
                ('agreement_date', models.DateField()),
                ('agreement', models.FileField(upload_to='agreementfile/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.state')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=12)),
                ('email_id', models.EmailField(max_length=50)),
                ('zip_code', models.CharField(max_length=50)),
                ('street', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.city')),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.client')),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.company')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoiceapp.state')),
            ],
        ),
    ]