# Generated by Django 4.1.6 on 2023-02-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0004_alter_author_born'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='text',
            field=models.CharField(max_length=1500, unique=True),
        ),
    ]
