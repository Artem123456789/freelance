# Generated by Django 4.0.6 on 2023-05-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_is_done_alter_order_is_employee_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderexecution',
            name='is_paid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]