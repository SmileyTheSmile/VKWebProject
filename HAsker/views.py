from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.list import MultipleObjectMixin

from HAsker.forms import SignUpForm, ProfileForm, AskForm, LoginForm
from HAsker.models import Profile, Question, Tag, Answer


# django-admin makemessages -l ru
# python manage.py compilemessages --use-fuzzy
    
    
class QuestionsView(ListView):
    template_name = 'questioning/index.html'
    paginate_by = 20
    model = Question
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }
    # TODO Fix long load times


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


class QuestionView(DetailView, MultipleObjectMixin):
    template_name = 'questioning/question.html'
    model = Question
    context_object_name = 'question'
    paginate_by = 5
    extra_context = {
        'popular_tags': Tag.objects.popular_tags(9),
        'popular_users': Profile.objects.popular_users(5),
    }

    def get_context_data(self, **kwargs):
        related_answers = Answer.objects.filter(question=self.get_object())
        context = super(QuestionView, self).get_context_data(object_list=related_answers, **kwargs)
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


def get_context_data_bad(self, **kwargs):
    related_answers = Answer.objects.filter(question=self.get_object())
    context = super(QuestionView, self).get_context_data(object_list=related_answers, **kwargs)
    context["tags"] = ''.join(
        [
            f'''<a class="btn btn-primary btn-sm mb-2 me-2 w-25 overflow-auto" href="#" role="button">
                { tag.name }
            </a>''' for tag in context["question"].tags.all()
        ]
    )
    '''
    <div class="row">
        {{ tags|safe  }}
    </div>
    '''
    return context