# Generated by Django 4.1.3 on 2023-01-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeekaki', '0024_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
