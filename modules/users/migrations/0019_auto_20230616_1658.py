# Generated by Django 3.2 on 2023-06-16 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_user_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscriptions',
            name='district',
        ),
        migrations.RemoveField(
            model_name='inscriptions',
            name='document_number',
        ),
        migrations.AddField(
            model_name='inscriptions',
            name='flag_business',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='inscriptions',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Puesto'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 16, 16, 58, 34, 905060), null=True, verbose_name='Última de modificación'),
        ),
    ]
