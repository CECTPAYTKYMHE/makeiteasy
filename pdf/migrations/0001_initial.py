# Generated by Django 4.0.4 on 2022-05-12 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=uuid.UUID('d24e19d7-2271-4a04-893e-b303921c7de6'), max_length=50, verbose_name='Имя файла')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('pdffile', models.FileField(blank=True, null=True, upload_to='pdf/%Y/%m/%d/', verbose_name='pdf файл')),
                ('zipimgfile', models.FileField(blank=True, null=True, upload_to='jpg/%Y/%m/%d/', verbose_name='jpgzip файл')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'PDF Файл',
                'verbose_name_plural': 'PDF Файлы',
            },
        ),
    ]
