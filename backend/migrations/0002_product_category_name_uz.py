# Generated by Django 4.0.4 on 2022-06-07 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_name_uz',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Category Ru'),
        ),
    ]