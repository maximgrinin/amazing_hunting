# Generated by Django 4.1.5 on 2023-01-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unknown', 'unknown'), ('employee', 'employee'), ('hr', 'hr')], default='unknown', max_length=8),
        ),
    ]