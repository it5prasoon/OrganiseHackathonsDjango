# Generated by Django 3.0.5 on 2020-05-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200519_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='question',
            field=models.FileField(default=1, upload_to='questions'),
            preserve_default=False,
        ),
    ]