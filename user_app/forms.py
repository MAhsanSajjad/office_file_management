
from django import forms
from django.contrib.auth import authenticate    
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255,required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter email', 'required':'true', 'autocomplete':'off'}))
    password = forms.CharField(required=True,  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'***********', 'required':'true', 'autocomplete':'off', 'aria-describedby':'password-addon'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        check_user = User.objects.filter(email=email).first()
        if not check_user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        print('*******************', check_user.username)
        user = authenticate(username=check_user.username, password=password)

        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(email=email).first()

        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        user = authenticate(username=user.username, password=password)
        return user


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name', 'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name', 'autocomplete': 'off'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'autocomplete': 'off'}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password', 'autocomplete': 'off'}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields did not match.')
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        username = self.cleaned_data.get('email').split('@')[0]
        user.username = username
        if commit:
            user.save()
        return user
