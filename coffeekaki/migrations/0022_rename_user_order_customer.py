# Generated by Django 4.1.3 on 2023-01-01 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffeekaki', '0021_alter_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='customer',
        ),
    ]
