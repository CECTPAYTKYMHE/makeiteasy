from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Login',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        }))
    
    class Meta:
        fields = ('username', 'password')
        
    def __init__(self, *args, **kwargs):
        super(UserLoginForm,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))
    captcha = CaptchaField(label='Введите символы')
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2','captcha')
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            
class UserProfileForm(UserChangeForm):
    """Форма для авторизации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True,}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True, }))
    
    class Meta:
        model = User
        fields = ['username', 'email']
     
    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'