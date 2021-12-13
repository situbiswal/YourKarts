from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext,gettext_lazy as _
from .models import Customer


class SignupForm(UserCreationForm):
    password1=forms.CharField( label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1', 'password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),}
        error_messages = {
            'username': {
                'unique': 'Your Custom Error Message here !!!',
            },}    


class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
    password=forms.CharField(strip=False,label=_('Password') ,widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password','autofocus':True}),strip=False,label=_('Old Password'))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password'}),strip=False,label=_('New Password'),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password'}),strip=False,label=_('Confirm New Password'))


class ChangePasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','autocomplete':'email'}),label=_('Email'),max_length=250)


class ChangePasswordConfirmForm(SetPasswordForm):
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password'}),strip=False,label=_('New Password'),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new-password'}),strip=False,label=_('Confirm New Password'))




class ProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }