
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, StudentUser
from main import models as mainmodels






class BootstrapPasswordInput(forms.PasswordInput):
    """
    Widget to apply Bootstrap styles to password input fields
    """
    template_name = 'django/forms/widgets/password.html'

class CustomerUserCreationForm(UserCreationForm):

    
    last_name = forms.CharField( label="Фамилия",max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label = "Имя",max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(label = "Отчество",max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label = "E-mail",required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    dateBith = forms.DateField(label = "Дата рождения",required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    customer = forms.ModelChoiceField(label = "Министрество",queryset= mainmodels.Customer.objects.all(), required = True, widget=forms.Select(attrs={'class': 'form-control'}))
    post = forms.CharField(label = "Должность",max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=BootstrapPasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=BootstrapPasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    
    class Meta:
        model = User
        fields =  ('last_name', 'first_name', 'patronymic','email', 'dateBith', 'password1', 'password2', 'customer', 'post')


    def clean(self):

        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Эта почта уже зарегистрирована")
            
        return cleaned_data

      
    

class StudentUserCreationForm(UserCreationForm):

    
    booknumber = forms.IntegerField(label = "Номер зачетной книжки",required = True, widget = forms.TextInput(attrs={ 'class': 'form-control'}))
    #email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=BootstrapPasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=BootstrapPasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    
    class Meta:
        model = User
        #fields =  ('email', 'booknumber', 'password1', 'password2',) 
        fields =  ('booknumber', 'password1', 'password2',) 
    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        booknumber = cleaned_data.get('booknumber')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Данная почта уже зарегистрирована")
        if StudentUser.objects.filter(booknumber = booknumber).exists():
            self.add_error("booknumber", "Студент с данным личным номером уже зареистрирован")
            

        return cleaned_data

    
class AuthCustomForm(AuthenticationForm):

    username  = forms.CharField( label="E-mail",max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=BootstrapPasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))

        
      
      