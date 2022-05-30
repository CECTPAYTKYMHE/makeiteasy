from django.urls import path
from .views import jpgtopdf, pdftotxt, Pdftojpg


urlpatterns = [
    path('pdftojpg/', Pdftojpg.as_view(), name='pdf'),
    path('jpgtopdf/', jpgtopdf, name='jpg'),
    path('pdftotxt/', pdftotxt, name='txt'),
]