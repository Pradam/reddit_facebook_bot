# Generated by Django 2.0.5 on 2018-06-01 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlinks',
            name='ups',
            field=models.IntegerField(default=0),
        ),
    ]
