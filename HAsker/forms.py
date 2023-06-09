from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from HAsker.models import Question, Answer, Profile, Tag

import django.forms as forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=256,
        required=True,
        label=_('EnterLogin'),
        #help_text=_('UsernameHelp'),
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
 
    def save(self, commit = True):
        user = super().save(commit)
        nickname = self.cleaned_data.get('nickname')
        new_profile = Profile.objects.create(
            user=user,
            nickname=nickname,
        )

        avatar = self.cleaned_data.get('avatar')
        if avatar:
            new_profile.avatar = avatar
            new_profile.save()
            
        return user
    
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
    
class ProfileSettingsForm(forms.ModelForm):
    nickname = forms.CharField(
        required=False,
        max_length=256,
        label=_('RegisterNickname'),
        widget=forms.TextInput(
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

    def save(self, commit = True):
        user = super().save(False)
        profile = user.profile
        profile.nickname = self.cleaned_data.get('nickname')
        profile.avatar = self.cleaned_data.get('avatar')
        profile.save()
            
        return user
    
    class Meta:
        model = User
        fields = [
            'nickname',
            'avatar', 
        ]   

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
        required=False,
        max_length=3000,
        label=_('QuestionTags'),
        widget=forms.TextInput(
            attrs= {
                'class': "form-control"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AskForm, self).__init__(*args, **kwargs)

    def save(self, commit = True):
        question = super().save(False)
        question.title = self.cleaned_data.get('title')
        question.content = self.cleaned_data.get('content')
        question.author = self.user.profile

        tagwords = list(map(lambda i:i.replace(" ", ""), self.cleaned_data.get('tags').split(',')))
        existing_tags = Tag.objects.filter(name__in=tagwords)
        existing_tagwords = [tag.name for tag in existing_tags]

        new_tags = []
        
        for tagword in tagwords:
            if not tagword in existing_tagwords:
                new_tag = Tag(name=tagword)
                new_tags.append(new_tag)
                existing_tagwords.append(new_tag.name)
        
        new_tags = Tag.objects.bulk_create(new_tags)
        new_tags.extend(existing_tags)

        question.save()
        question.tags.set(new_tags)
            
        return question

    class Meta: 
        model = Question
        fields = (
            'title',
            'content',
            'tags',
        )
    

class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        max_length=30000,
        label=_('AnswerContent'),
        widget=forms.Textarea(
            attrs= {
                'class': "form-control",
                "rows":"10",
            }
        ), 
    )

    class Meta: 
        model = Answer
        fields = (
            'content',
        )