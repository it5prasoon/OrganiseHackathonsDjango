# Generated by Django 3.0.6 on 2020-05-15 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200515_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='daysleft',
            new_name='daysLeft',
        ),
    ]
