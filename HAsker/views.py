from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import date

from django.contrib.auth.views import LoginView
from django.views.generic import View, CreateView, UpdateView

from HAsker.ui_text import UI_TEXT
from HAsker.forms import SignInForm, SignUpForm, ProfileForm
from HAsker.models import QuestionManager, TagManager, UserManager, User


class SignInView(LoginView):
    redirect_authenticated_user = True
    authentication_form = SignInForm
    extra_context = UI_TEXT['ru']
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    def form_invalid(self, form):
        messages.error(self.request,UI_TEXT['ru']["login_failed"])
        return self.render_to_response(self.get_context_data(form=form))
    
class QuestionView(View):
    pass

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'commons/profile.html'


def index(request):
    context = {
            'data':
                {
                    'account':
                        {
                            'login': 'kdanil01',
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'questions': QuestionManager.recent_questions(20),
                    'popular_tags': TagManager.popular_tags(9),
                    'popular_users': UserManager.popular_users(5),
                },
            'ui_text': UI_TEXT['ru'],
        }
    template = 'index.html'
    return render(request, template, context)


def question(request, question_id):
    context = {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': TagManager.popular_tags(5),
                    'popular_users': UserManager.popular_users(5),
                },
            'ui_text': UI_TEXT['ru'],
        }
    template = 'question.html'
    return render(request, template, context)


def sign_up(request):
    context = {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': TagManager.popular_tags(5),
                    'popular_users': UserManager.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    template = 'signup.html'
    return render(request, template, context)


@login_required(redirect_field_name='login')
def ask_question(request): 
    return render(
        request,
        'ask.html',
        {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': TagManager.popular_tags(5),
                    'popular_users': UserManager.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )

