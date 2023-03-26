from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import date

from HASKer.ui_text import UI_TEXT
from HASKer.models import DummyInfo


def get_questions(request):
    return render(
        request,
        'index.html',
        {
            'data':
                {
                    'account':
                        {
                            'login': 'kdanil01',
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'questions': DummyInfo.questions_list(20),
                    'popular_tags': DummyInfo.popular_tags(9),
                    'popular_users': DummyInfo.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )


def get_question(request, question_id):
    return render(
        request,
        'blocks/question.html',
        {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': DummyInfo.popular_tags(5),
                    'popular_users': DummyInfo.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )


def get_login(request):
    return render(
        request,
        'login.html',
        {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': DummyInfo.popular_tags(9),
                    'popular_users': DummyInfo.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )


def sign_up(request):
    return render(
        request,
        'signup.html',
        {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'popular_tags': DummyInfo.popular_tags(5),
                    'popular_users': DummyInfo.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )


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
                    'popular_tags': DummyInfo.popular_tags(5),
                    'popular_users': DummyInfo.popular_users(5),
                    'links': {},
                },
            'ui_text': UI_TEXT['ru'],
        }
    )

