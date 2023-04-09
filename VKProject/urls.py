from django.contrib import admin
from django.urls import path

from HAsker import views
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView
)
from HAsker.ui_text import UI_TEXT


urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('admin/',
         admin.site.urls,
         name='admin'),
    path('question/<int:id>/',
         views.question,
         name='question_url'),
    path('login/',
         views.SignInView.as_view(next_page='index'),
         name='login'),
    path('profile/<int:pk>/',
         views.SignInView.as_view(),
         name='profile'),
    path('password_reset/',
         PasswordResetView.as_view(),
         name='password_reset'),
    path('logout/',
         LogoutView.as_view(next_page='login'),
         name='logout'),
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),
    path('ask/',
         views.ask_question,
         name='ask'),
]
