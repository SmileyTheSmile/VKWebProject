from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from HAsker.models import Question

import django.forms as forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=256,
        required=True,
        label=_('EnterLogin'),
        help_text=_('UsernameHelp'),
        widget=forms.EmailInput(
            attrs= {
                'class': "form-control",
                'placeholder': _('LoginPlaceholder')
            }
        ),
    )
    password = forms.CharField(
        max_length=256,
        required=True,
        label=_('EnterPassword'),
        help_text=_('PasswordHelp'),
        widget=forms.PasswordInput(
            attrs= {
                'class': "form-control",
                'placeholder': _('PasswordPlaceholder')
            }
        ),
    )
    stay_logged_in = forms.BooleanField(
        label=_('RememberPassword'),
        required=False,
        widget=forms.CheckboxInput(
            attrs= {
                'class': "form-check-input"
            },
        ),
    )

class SignUpForm(UserCreationForm):
    username = UsernameField(
        required=True,
        max_length=256,
        label=_('RegisterUsername'),
        widget=forms.TextInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    email = forms.CharField(
        required=True,
        max_length=320,
        label=_('RegisterEmail'),
        widget=forms.EmailInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    nickname = forms.CharField(
        required=True,
        max_length=256,
        label=_('RegisterNickname'),
        widget=forms.TextInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    password1 = forms.CharField(
        required=True,
        max_length=256,
        label=_('RegisterPassword1'),
        widget=forms.PasswordInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        max_length=256,
        label=_('RegisterPassword2'),
        widget=forms.PasswordInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        label=_('UploadAvatar'),
        widget=forms.FileInput(
            attrs= {
                'class': "btn btn-outline"
            }
        ),
    )
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email',
            'nickname',
            'password1', 
            'password2', 
            'avatar', 
        ]

class ProfileForm(forms.ModelForm):
    pass

class AskForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        max_length=256,
        label=_('QuestionTitle'),
        widget=forms.TextInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )
    content = forms.CharField(
        required=True,
        max_length=30000,
        label=_('QuestionContent'),
        widget=forms.Textarea(
            attrs= {
                'class': "form-control",
                "rows":"10",
            }
        ),
    )
    tags = forms.CharField(
        max_length=3000,
        label=_('QuestionTags'),
        widget=forms.TextInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )

    class Meta: 
        model = Question
        fields = (
            'title',
            'content',
            'tags',
        )