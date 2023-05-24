from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from HAsker import views
from django.views.generic import RedirectView
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
)

urlpatterns = [
     path('',
          RedirectView.as_view(pattern_name='questions', permanent=False),
          name='index'),
     path('questions/',
          views.QuestionsView.as_view(),
          name='questions'),
     path('questions/<str:order>/',
          views.QuestionsView.as_view(),
          name='questions_ordered'),
     path('questions/tags/<int:tag>/',
          views.QuestionsView.as_view(),
          name='questions_tagged'),
     path('admin/',
          admin.site.urls,
          name='admin'),
     path('login/',
          views.SignInView.as_view(),
               name='login',),
     path('logout/',
          LogoutView.as_view(next_page='login'),
          name='logout'),
     path('signup/',
          views.SignUpView.as_view(),
          name='signup'),
     path('question/<int:pk>/',
          views.QuestionView.as_view(),
          name='question'),
     path('profile/<int:pk>/',
          views.ProfileView.as_view(),
          name='profile'),
     path('settings/',
          views.ProfileSettingsView.as_view(),
          name='profile_settings'),
     path('password_reset/',
          PasswordResetView.as_view(),
          name='password_reset'),
     path('ask/',
          views.AskView.as_view(),
          name='ask'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)