# Generated by Django 4.0.5 on 2022-06-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_remove_order_aksiya_product_aksiya'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Photo'),
        ),
    ]