# Generated by Django 4.1.5 on 2023-01-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeekaki', '0029_rename_show_history_state_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='table_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
