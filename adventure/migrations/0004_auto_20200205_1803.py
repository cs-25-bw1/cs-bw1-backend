# Generated by Django 3.0.3 on 2020-02-05 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0003_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='map_string',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=10000),
        ),
    ]
