from django.contrib import admin
from django.urls import path

from HAsker import views, forms
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
)


urlpatterns = [
    path('',
         views.QuestionsView.as_view(),
         name='index'),
    path('admin/',
         admin.site.urls,
         name='admin'),
    path('login/',
         LoginView.as_view(
          authentication_form=forms.LoginForm,
          next_page='index'),
          name='login'),
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
    path('password_reset/',
         PasswordResetView.as_view(),
         name='password_reset'),
    path('ask/',
         views.AskView.as_view(),
         name='ask'),
]
