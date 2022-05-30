from django.urls import path
from .views import Pdftojpg, Jpgtopdf, Pdftotxt


urlpatterns = [
    path('pdftojpg/', Pdftojpg.as_view(), name='pdf'),
    path('jpgtopdf/', Jpgtopdf.as_view(), name='jpg'),
    path('pdftotxt/', Pdftotxt.as_view(), name='txt'),
]