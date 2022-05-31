from .models import Pdf
from django import forms

class PdfForm(forms.ModelForm):
    """Форма загрузки файлов для модели models.Pdf"""
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'form-control',
               'placeholder': "Для отображения в личном кабинете, не обязательное поле"}))
    pdffile = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'formFileMultiple',
               'class':'form-control',
               'multiple': True}))

    class Meta:
        model = Pdf
        fields = ('name', 'pdffile')
        
class TxtForm(forms.ModelForm):
    """Форма загрузки файлов с выбором языка для модели models.Pdf"""
    CHOICES = [('eng', 'Английский'), ('rus', 'Русский')]
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'form-control',
               'placeholder': "Для отображения в личном кабинете, не обязательное поле"}))
    pdffile = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'formFileMultiple',
               'class':'form-control',
               'multiple': True,
                }))
    lang = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}),choices=CHOICES)

    class Meta:
        model = Pdf
        fields = ('name', 'pdffile', 'lang')
    
    
    