from django.urls import path
from .views import pdftojpg, jpgtopdf


urlpatterns = [
    path('pdftojpg/', pdftojpg, name='pdf'),
    path('jpgtopdf/', jpgtopdf, name='jpg'),
]