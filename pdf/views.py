import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from makeiteasy.settings import BASE_DIR
from .forms import PdfForm
from .models import Pdf
import os
from zipfile import ZipFile
from pdf2image import convert_from_bytes
import shutil
from datetime import date
from pathlib import Path
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

media = os.path.join(BASE_DIR, 'media/')
 
def pdftojpg(request):
    """View функция для отправки и сохранения PDF файлов(принимает только PDF файлы остальные отбрасывает) с 
    последующим преобразованием в JPG zip архив"""
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
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
            for afile in request.FILES.getlist('pdffile'):
                if afile.content_type != 'application/pdf':
                    continue
                file_obj = Pdf.objects.create(name=name, pdffile=afile, user = user)
                Pdf.objects.filter(pk=file_obj.id).update(zipimgfile = pdfjpgconvert(afile))
                url = Pdf.objects.get(pk=file_obj.id)
                jpgziplist.append({'url' : url.zipimgfile.url,
                                   'name': str(url.pdffile).split('/')[-1]})
            context = {
                'urls' : jpgziplist,
                'back' : "/pdf/pdftojpg"
            }
            return render(request, 'pdf/readyfiles.html', context)
    else:
        form = PdfForm()
    context = {
        'title': 'pdf',
        'form': form,
    }
    return render(request, 'pdf/pdf.html', context)

def pdfjpgconvert(file):
    """Конвертер из PDF в JPG и архивирования JPG файлов в ZIP 
    возвращает расположение ZIP JPG файла"""
    file.open()
    pages = convert_from_bytes(file.read(), 500, poppler_path='D:/django/poppler-22.04.0/Library/bin')
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

def jpgtopdf(request):
    """View функция для отправки и сохранения ZIP JPG файлов с 
    последующим преобразованием в PDF"""
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if request.POST['name'] != '':
            name = '(JPGtoPDF) ' + request.POST['name']
        else:
            name = '(JPGtoPDF) ' + str(uuid.uuid4())
        if request.user.is_anonymous:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        if form.is_valid():
            pdflist = []
            jpgziplist = request.FILES.getlist('pdffile')
            pdf, jpg = jpgpdfconverter(jpgziplist)
            file_obj = Pdf.objects.create(name=name, pdffile=pdf, zipimgfile=jpg, user=user)
            pdflist.append({'url' : file_obj.pdffile.url,
                            'name': str(file_obj.pdffile).split('/')[-1]
                            })
            context = {
                'urls' : pdflist,
                'back' : "/pdf/jpgtopdf"
            }
            return render(request, 'pdf/readyfiles.html', context)
    else:
        form = PdfForm()
    context = {
        'title': 'pdf',
        'form': form,
    }
    return render(request, 'pdf/img.html', context)

def jpgpdfconverter(jpgrawlst):
    """Конвертер из JPG в PDF(принимает только файлы изображений, остальные файлы отбрасывает),
    возвращает расположение PDF и ZIP JPG файла"""
    lst = []
    i = 1
    current_date = date.today()
    Path(media + 'jpg/' + str(current_date)).mkdir(parents=True, exist_ok=True)
    jpgzipname = f'jpg/{str(current_date)}/{uuid.uuid4()}.zip'
    # folder = uuid.uuid4()
    # os.mkdir(media + f'jpg/temp/{folder}')
    with ZipFile(media + jpgzipname, 'a') as myzip:
        for file in jpgrawlst:
            if 'image' not in file.content_type:
                    continue
            lst.append(Image.open(file).convert('RGB'))
            file.open()
            myzip.writestr(data=file.read(),zinfo_or_arcname=f'{i}.jpg')
            file.close()
            i += 1
    # shutil.rmtree(media + f'jpg/temp/{folder}')
    myzip.close()
    Path(media + 'pdf/converted/' + str(current_date)).mkdir(parents=True, exist_ok=True)
    pdfname = f'pdf/converted/{str(current_date)}/{uuid.uuid4()}.pdf'
    lst[0].save(media + pdfname, save_all=True, append_images=lst[1:])
    return pdfname, jpgzipname

def pdftotextconverter(pdf,lang):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    pdf.open()
    pages = convert_from_bytes(pdf.read(), 500,poppler_path='D:/django/poppler-22.04.0/Library/bin')
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

def pdftotxt(request):
    """View функция для отправки и сохранения PDF файлов(принимает только PDF файлы остальные отбрасывает) с 
    последующим преобразованием и распознованием текста в TXT zip архив"""
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
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
                Pdf.objects.filter(pk=file_obj.id).update(zipimgfile = pdftotextconverter(afile,'rus'))
                url = Pdf.objects.get(pk=file_obj.id)
                jpgziplist.append({'url' : url.zipimgfile.url,
                                   'name': str(url.pdffile).split('/')[-1]})
            context = {
                'urls' : jpgziplist,
                'back' : "/pdf/pdftotxt"
            }
            return render(request, 'pdf/readyfiles.html', context)
    else:
        form = PdfForm()
    context = {
        'title': 'txt',
        'form': form,
    }
    return render(request, 'pdf/txt.html', context)

    

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

