from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.utils.translation import gettext as _

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin

from HAsker.forms import SignUpForm, ProfileSettingsForm, AskForm, AnswerForm, LoginForm
from HAsker.models import Profile, Question, Tag, Answer


# django-admin makemessages -l ru
# python manage.py compilemessages --use-fuzzy
    
    
class QuestionsView(ListView):
    template_name = 'questioning/index.html'
    paginate_by = 20
    model = Question
    ordering = "-rating"
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
        'ordering_masks': {
            "new": {
                "sort_field": "date_published",
                "label": _("NewQuestions"),
            },
            "top": {
                "sort_field": "-rating",
                "label": _("PopularQuestions")
            },
        }
    }

    def get_queryset(self):
        tag = self.kwargs.get('tag', None)
        queryset = Question.objects.questions_by_tag(tag) if tag else super().get_queryset()
        return queryset

    def get_ordering(self):
        ordering_type = self.kwargs.get('order', "new")
        self.ordering = self.extra_context['ordering_masks'][ordering_type]["sort_field"]
        return self.ordering

    
class AskView(CreateView, LoginRequiredMixin):
    template_name = 'questioning/ask.html'
    login_url = "login"
    model = Question
    form_class = AskForm
    success_url = reverse_lazy('index')
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }


class QuestionView(DetailView, MultipleObjectMixin, FormMixin):
    template_name = 'questioning/question.html'
    model = Question
    form_class = AnswerForm
    context_object_name = 'question'
    success_url = None
    paginate_by = 5
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }

    def get_context_data(self, **kwargs):
        related_answers = Answer.objects.filter(question=self.get_object())
        context = super(QuestionView, self).get_context_data(object_list=related_answers,
                                                             **kwargs)
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


class SignInView(LoginView):
    form_class = LoginForm
    next_page='index'
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }
    # TODO Correctly check if the fields are correct
    # TODO Fix authorization


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile_edit.html'
    model = User
    form_class = ProfileSettingsForm
    success_url = reverse_lazy('index')
    context_object_name = 'user'
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }

    def get_object(self, queryset=None):
        user = self.request.user
        profile = user.profile
        self.initial['nickname'] = profile.nickname
        self.initial['avatar'] = profile.avatar
        return user


class ProfileView(DetailView):
    template_name = 'registration/profile.html'
    model = Profile
    context_object_name = 'profile'
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }

