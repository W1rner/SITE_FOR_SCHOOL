# Generated by Django 3.1.4 on 2020-12-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.CharField(default=100, max_length=100),
            preserve_default=False,
        ),
    ]