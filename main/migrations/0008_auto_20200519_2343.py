# Generated by Django 3.0.5 on 2020-05-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200519_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Job',
            field=models.IntegerField(choices=[(1, 'Organiser'), (2, 'Participant')], default=2),
        ),
    ]
