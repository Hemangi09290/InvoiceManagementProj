# Generated by Django 3.2.5 on 2022-09-12 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoiceapp', '0051_auto_20220909_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='developer',
            field=models.ManyToManyField(null=True, related_name='developer', to='invoiceapp.Developer'),
        ),
    ]