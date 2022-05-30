from django.urls import path
from .views import login, register, logout_user, profile, profile_pdf
from pdf.views import PDFDeleteView, massdelete

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/pdf', profile_pdf, name='profile_pdf'),
    path('logout/', logout_user, name='logout'),
    path('delete/<int:pk>/', PDFDeleteView.as_view(), name='delete'),
    path('chkdelete/', massdelete, name='massdelete'),
]

