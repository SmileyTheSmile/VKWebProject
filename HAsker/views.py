from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, FormView, ListView
from django.views.generic.base import TemplateView

from HAsker.ui_text import UI_TEXT
from HAsker.forms import LoginForm, SignUpForm, ProfileForm, AskForm
from HAsker.models import QuestionManager, TagManager, UserManager, Profile, Question


# django-admin makemessages -l ru
# python manage.py compilemessages --use-fuzzy


class SignInView(LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm
    extra_context = {
        'questions': QuestionManager.recent_questions(20),
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    def form_invalid(self, form):
        messages.error(self.request,UI_TEXT['ru']["login_failed"])
        return self.render_to_response(self.get_context_data(form=form))
    
class QuestionsView(ListView):
    template_name = 'index.html'
    paginate_by = 10
    model = Question
    extra_context = {
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class AskView(CreateView, LoginRequiredMixin):
    template_name = 'ask.html'
    login_url = "login"
    model = Question
    form_class = AskForm
    success_url = reverse_lazy('index')
    extra_context = {
        'questions': QuestionManager.recent_questions(20),
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }

class QuestionView(TemplateView):
    login_url = "question"
    success_url = reverse_lazy('index')
    template_name = 'question.html'
    extra_context = {
        'questions': QuestionManager.recent_questions(30),
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    extra_context = {
        'questions': QuestionManager.recent_questions(20),
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }
    
class ProfileView(UpdateView):
    template_name = 'commons/profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    extra_context = {
        'questions': QuestionManager.recent_questions(20),
        'popular_tags': TagManager.popular_tags(9),
        'popular_users': UserManager.popular_users(5),
    }
