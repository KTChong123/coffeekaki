# Generated by Django 4.1.3 on 2022-12-25 15:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coffeekaki', '0004_order_product_user_orderupdate_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='catergory',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
