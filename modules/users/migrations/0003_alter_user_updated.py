# Generated by Django 3.2 on 2023-06-14 04:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 13, 23, 31, 22, 9985), null=True, verbose_name='Última de modificación'),
        ),
    ]
