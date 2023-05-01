from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, FormView, ListView
from django.views.generic.detail import DetailView

from HAsker.ui_text import UI_TEXT
from HAsker.forms import LoginForm, SignUpForm, ProfileForm, AskForm
from HAsker.models import Profile, Question, Tag, Answer


# django-admin makemessages -l ru
# python manage.py compilemessages --use-fuzzy


class SignInView(LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    def form_invalid(self, form):
        messages.error(self.request,UI_TEXT['ru']["login_failed"])
        return self.render_to_response(self.get_context_data(form=form))
    
    
class QuestionsView(ListView):
    template_name = 'questioning/index.html'
    paginate_by = 20
    model = Question
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }
    

class AskView(CreateView, LoginRequiredMixin):
    template_name = 'questioning/ask.html'
    login_url = "login"
    model = Question
    form_class = AskForm
    success_url = reverse_lazy('index')
    extra_context = {
        'questions': Question.objects.recent_questions(20),
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }


class QuestionView(ListView):
    template_name = 'questioning/question.html'
    model = Answer
    context_object_name = 'question'
    paginate_by = 5
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(QuestionView, self).get(request, *args, **kwargs)

    def get_queryset_for_object(self, pk):
        return Question.objects.question_by_id(pk)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            raise AttributeError('pk expected in url')
        queryset = self.get_queryset_for_object(pk)
        return get_object_or_404(queryset, pk=pk)

    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        return context


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }
    

class ProfileEditView(UpdateView):
    template_name = 'registration/profile_edit.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }


class ProfileView(DetailView):
    template_name = 'registration/profile.html'
    model = Profile
    context_object_name = 'profile'
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }