import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from makeiteasy.settings import BASE_DIR
from .forms import PdfForm, TxtForm
from .models import Pdf
import os
from zipfile import ZipFile
from pdf2image import convert_from_bytes
import shutil
from datetime import date
from pathlib import Path
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView
from PIL import Image
import pytesseract
from django.views import View

media = os.path.join(BASE_DIR, 'media/')
 
class Pdftojpg(View):
    """Class View функция для отправки и сохранения PDF файлов(принимает только PDF файлы остальные отбрасывает) с 
    последующим преобразованием в JPG zip архив"""
    
    form_class = PdfForm
    template_name = 'pdf/pdf.html'
    
    def get(self, request,  *args, **kwargs):
        context = {
        'title': 'PDFtoJPG',
        'form': self.form_class,
    }
        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.POST['name'] != '':
            name = '(PDFtoJPG) ' + request.POST['name']
        else:
            name = '(PDFtoJPG) ' + str(uuid.uuid4())
        if request.user.is_anonymous:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        if form.is_valid():
            jpgziplist = []
            for file in request.FILES.getlist('pdffile'):
                if file.content_type != 'application/pdf':
                    continue
                file_obj = Pdf.objects.create(name=name, pdffile=file, user = user)
                Pdf.objects.filter(pk=file_obj.id).update(zipimgfile = self.pdfjpgconvert(file))
                url = Pdf.objects.get(pk=file_obj.id)
                jpgziplist.append({'url' : url.zipimgfile.url,
                                   'name': str(url.pdffile).split('/')[-1]})
            context = {
                'urls' : jpgziplist,
                'back' : "/pdf/pdftojpg",
            }
            return render(request, 'pdf/readyfiles.html', context)
        
    def pdfjpgconvert(self, file):
        """Конвертер из PDF в JPG и архивирования JPG файлов в ZIP 
            возвращает расположение ZIP JPG файла"""
        file.open()
        pages = convert_from_bytes(file.read(), 500)
        file.close()
        i = 1
        current_date = date.today()
        Path(media + 'jpg/converted/' + str(current_date)).mkdir(parents=True, exist_ok=True)
        jpgzipname = f'jpg/converted/{str(current_date)}/{uuid.uuid4()}.zip'
        with ZipFile(media + jpgzipname, 'w') as myzip:
            for page in pages:
                folder = uuid.uuid4()
                os.mkdir(media + f'pdf/temp/{folder}')
                page.save(media + f'pdf/temp/{folder}/{i}.jpg')
                myzip.write(media + f'pdf/temp/{folder}/{i}.jpg',arcname=f'{i}.jpg')
                i += 1
        shutil.rmtree(media + f'pdf/temp/{folder}')
        myzip.close()
        return jpgzipname   


class Jpgtopdf(View):
    """Class View функция для отправки JPG и сохранения в ZIP файлы с 
    последующим преобразованием в PDF"""
    form_class = PdfForm
    template_name = 'pdf/img.html'
    
    def get(self, request,  *args, **kwargs):
        context = {
        'title': 'JPGtoPDF',
        'form': self.form_class,
    }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.POST['name'] != '':
            name = '(PDFtoJPG) ' + request.POST['name']
        else:
            name = '(PDFtoJPG) ' + str(uuid.uuid4())
        if request.user.is_anonymous:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        if form.is_valid():
            pdflist = []
            err = 0 # маркер проверки валидности файлов
            jpgziplist = request.FILES.getlist('pdffile')
            for afile in jpgziplist:
                if 'image' not in afile.content_type:
                    err += 1
                if err == len(jpgziplist):
                    messages.warning(request, "Неверные файлы")
                    return HttpResponseRedirect(reverse('pdf:jpg'))
            pdf, jpg = self.jpgpdfconverter(jpgziplist)
            file_obj = Pdf.objects.create(name=name, pdffile=pdf, zipimgfile=jpg, user=user)
            pdflist.append({'url' : file_obj.pdffile.url,
                            'name': str(file_obj.pdffile).split('/')[-1]
                            })
            context = {
                'urls' : pdflist,
                'back' : "/pdf/jpgtopdf"
            }
            return render(request, 'pdf/readyfiles.html', context)

    def jpgpdfconverter(self, jpgrawlst):
        """Конвертер из JPG в PDF(принимает только файлы изображений, остальные файлы отбрасывает),
        возвращает расположение PDF и ZIP JPG файла"""
        lst = []
        i = 1
        current_date = date.today()
        Path(media + 'jpg/' + str(current_date)).mkdir(parents=True, exist_ok=True)
        jpgzipname = f'jpg/{str(current_date)}/{uuid.uuid4()}.zip'
        with ZipFile(media + jpgzipname, 'a') as myzip:
            for file in jpgrawlst:
                if 'image' not in file.content_type:
                    continue
                lst.append(Image.open(file).convert('RGB'))
                file.open()
                myzip.writestr(data=file.read(),zinfo_or_arcname=f'{i}.jpg')
                file.close()
                i += 1
        myzip.close()
        Path(media + 'pdf/converted/' + str(current_date)).mkdir(parents=True, exist_ok=True)
        pdfname = f'pdf/converted/{str(current_date)}/{uuid.uuid4()}.pdf'
        lst[0].save(media + pdfname, save_all=True, append_images=lst[1:])
        return pdfname, jpgzipname


class Pdftotxt(View):
    """Class View функция для отправки и сохранения PDF файлов(принимает только PDF файлы остальные отбрасывает) с 
    последующим преобразованием и распознованием текста в TXT zip архив"""
    form_class = TxtForm
    template_name = 'pdf/txt.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'PDFtoTXT',
            'form': self.form_class,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if request.POST['name'] != '':
            name = '(PDFtoTXT) ' + request.POST['name']
        else:
            name = '(PDFtoTXT) ' + str(uuid.uuid4())
        if request.user.is_anonymous:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        if form.is_valid():
            jpgziplist = []
            for afile in request.FILES.getlist('pdffile'):
                if afile.content_type != 'application/pdf':
                    continue
                file_obj = Pdf.objects.create(name=name, pdffile=afile, user = user)
                Pdf.objects.filter(pk=file_obj.id).update(zipimgfile = self.pdftotextconverter(afile,request.POST['lang']))
                url = Pdf.objects.get(pk=file_obj.id)
                jpgziplist.append({'url' : url.zipimgfile.url,
                                   'name': str(url.pdffile).split('/')[-1]})
            context = {
                'urls' : jpgziplist,
                'back' : '/pdf/pdftotxt',
            }
            return render(request, 'pdf/readyfiles.html', context)
   
    def pdftotextconverter(self, pdf, lang):
        """Конвертет из PDF в TXT, каждая страница отдельный TXT файл, с распознованием текста(Англ и Рус языки), 
        возвращает расположение txt zip файла"""
        pdf.open()
        pages = convert_from_bytes(pdf.read(), 500)
        pdf.close()
        current_date = date.today()
        Path(media + 'txt/' + str(current_date)).mkdir(parents=True, exist_ok=True)
        txtzipname = f'txt/{str(current_date)}/{uuid.uuid4()}.zip'
        folder = uuid.uuid4()
        os.mkdir(media + f'txt/temp/{folder}')
        for pageNum,imgBlob in enumerate(pages):
            text = pytesseract.image_to_string(imgBlob,lang=lang)
            with ZipFile(media + txtzipname, 'a') as myzip:
                with open(media + f'txt/temp/{folder}/{pageNum}.txt', 'w') as the_file:
                    the_file.write(text)
                    the_file.close()
                myzip.write(media + f'txt/temp/{folder}/{pageNum}.txt',arcname=f'page_{pageNum}.txt')
        shutil.rmtree(media + f'txt/temp/{folder}')
        return txtzipname


class PDFDeleteView(SuccessMessageMixin, DeleteView):
    """Класс для штучного удаления файлов из Личного кабинета пользователя"""
    model = Pdf
    template_name = 'users/profile_delete.html'
    extra_context = {'title' : 'Удаление файла'}
    success_url = reverse_lazy('users:profile_pdf')
    success_message = 'Файл успешно удален'
    

def massdelete(request):
    """Функция масового удаления файлов из личного кабинета пользователя"""
    if request.method == 'POST':
        todeletelsts = request.POST.getlist('choices')
        for todeletelst in todeletelsts:
            Pdf.objects.filter(pk=todeletelst).delete()
    return HttpResponseRedirect(reverse('users:profile_pdf'))

