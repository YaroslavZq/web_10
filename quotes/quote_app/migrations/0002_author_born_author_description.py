# Generated by Django 4.1.6 on 2023-02-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='born',
            field=models.CharField(default='born', max_length=50),
        ),
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.CharField(default='description', max_length=5000),
        ),
    ]
