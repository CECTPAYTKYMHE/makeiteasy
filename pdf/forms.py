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
    
    # def __init__(self, user, *args, **kwargs):
    #     super(PdfForm, self).__init__(*args, **kwargs)
    #     if user.is_anonymous:
    #         self.fields['name'].widget.attrs['disabled'] = True
    #         self.fields['name'].widget.attrs['placeholder'] = 'Поле не доступно для не авторизованных пользователей'
    
    