# Generated by Django 3.2.15 on 2022-09-08 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0021_alter_customer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='customer',
        ),
    ]