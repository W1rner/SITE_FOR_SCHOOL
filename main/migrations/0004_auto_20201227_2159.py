# Generated by Django 3.1.4 on 2020-12-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201227_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.CharField(default=100, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default=100, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]