from django.contrib import admin
from .models import Pdf
# Register your models here.

class PdfAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_created')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('pdffile', 'zipimgfile')

    
admin.site.register(Pdf, PdfAdmin)