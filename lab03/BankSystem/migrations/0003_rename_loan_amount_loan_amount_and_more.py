# Generated by Django 4.0.4 on 2022-06-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankSystem', '0002_alter_loan_loan_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='loan_amount',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='loan_status',
        ),
        migrations.AddField(
            model_name='loan',
            name='lstatus',
            field=models.CharField(choices=[('unissue', 'unissue'), ('issuing', 'issuing'), ('issued', 'issued')], default='unissue', max_length=20),
        ),
    ]