# Generated by Django 4.1.5 on 2023-01-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='f', max_length=1),
        ),
    ]