# Generated by Django 4.0.4 on 2022-05-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя файла'),
        ),
    ]
