# Generated by Django 3.0.6 on 2020-05-14 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lists',
            name='daysleft',
            field=models.BooleanField(default=True),
        ),
    ]
