# Generated by Django 3.0.5 on 2020-05-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='images',
            field=models.ImageField(blank=True, upload_to='profileImage'),
        ),
    ]
