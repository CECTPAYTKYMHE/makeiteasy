import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Pdf(models.Model):
    """Модель для преобразования PDF в JPG и обратно"""
    name = models.CharField(max_length=50,verbose_name='Имя файла')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    pdffile = models.FileField(upload_to='pdf/%Y/%m/%d/', verbose_name='pdf файл', blank=True, null=True)
    zipimgfile = models.FileField(upload_to='jpg/%Y/%m/%d/', verbose_name='jpgzip файл',blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    class Meta:
        verbose_name = 'PDF Файл'
        verbose_name_plural = 'PDF Файлы'
    
    def pdfname(self):
        return os.path.basename(self.pdffile.name)
    
    def __str__(self):
        return self.name
    
@receiver(models.signals.post_delete, sender=Pdf)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Удаление файла когда удаляется запись в базе"""
    if instance.pdffile:
        if os.path.isfile(instance.pdffile.path):
            os.remove(instance.pdffile.path)
    if instance.zipimgfile:
        if os.path.isfile(instance.zipimgfile.path):
            os.remove(instance.zipimgfile.path)
    
    

    