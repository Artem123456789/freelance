# Generated by Django 4.0.6 on 2023-05-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_orderexecution_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime_compelete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='datetime_employee_selected',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='deadline_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
