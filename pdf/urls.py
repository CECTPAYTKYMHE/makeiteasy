from django.urls import path
from .views import pdftojpg, jpgtopdf, pdftotxt


urlpatterns = [
    path('pdftojpg/', pdftojpg, name='pdf'),
    path('jpgtopdf/', jpgtopdf, name='jpg'),
    path('pdftotxt/', pdftotxt, name='txt'),
]