# Generated by Django 5.2 on 2025-04-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_transaction_reference_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reference_number',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
