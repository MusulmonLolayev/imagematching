# Generated by Django 3.1.4 on 2021-01-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210117_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='name',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
