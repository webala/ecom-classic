# Generated by Django 4.1.1 on 2022-11-11 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='estate',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='house_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
