from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm, UsernameField
from HAsker.ui_text import UI_TEXT
from django.contrib.auth.models import User

import django.forms as forms


class SignInForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = UI_TEXT['ru']["register_login"]
        self.fields['password'].label = UI_TEXT['ru']["register_password"]
        
        self.fields['password'].help_text = "xcxc"
        self.fields['password'].help_text = "xcxc"
        
        for key, item in self.fields.items():
            print(f"{key}, {item}")
        
        self.fields['username'].widget.attrs = {
                'class': 'form-control',
                'placeholder': UI_TEXT['ru']["login_hint"]
            }
        self.fields['password'].widget.attrs = {
                'class': 'form-control'
            }
        
        self.fields['stay_logged_in'] = forms.BooleanField(required=False,
                                                           help_text=UI_TEXT['ru']["stay_logged_in"],
                                                           )
        self.fields['stay_logged_in'].widget.attrs = {
            'class': "form-check-input"
        }

class SignUpForm(BaseUserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    username = UsernameField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = {
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'username',
            'first_name', 
            'last_name', 
            'email',
        }
        
        widgets = {
            'username': forms.TextInput(
            attrs=
            {
                'class': 'form-control'
            }),
            'first_name':forms.TextInput(
            attrs=
            {
                'class': 'form-control'
            }),
            'last_name':forms.TextInput(
            attrs=
            {
                'class': 'form-control'
            }), 
            'email':forms.TextInput(
            attrs=
            {
                'class': 'form-control'
            }),
        }