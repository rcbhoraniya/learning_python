# Generated by Django 3.2.5 on 2021-08-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toris', '0004_alter_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='req_denier',
            field=models.CharField(max_length=10, verbose_name='Denier'),
        ),
    ]
