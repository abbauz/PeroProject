# Generated by Django 4.0.4 on 2022-06-13 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_cashback_options_alter_location_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='aksiya',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
