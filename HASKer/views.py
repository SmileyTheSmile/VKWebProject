from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from HASKer.text import UI_TEXT
import lorem


def get_questions(request):
    questions_per_page = 20
    popular_accounts_num = 5
    popular_tags_num = 5

    questions_list = [
        {
            'id': i,
            'title': f'Вопрос #{i}: {lorem.sentence()}',
            'description': lorem.text(),
            'rating': 5,
            'account':
                {
                    'login': f'{lorem.sentence().split()[0]}{i}',
                    'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                }
        }
        for i in range(questions_per_page)]

    popular_tags = [
        {
            'text': lorem.sentence().split()[0],
            'id': i
        }
        for i in range(popular_tags_num)]

    popular_accounts = [
        {
            'login': lorem.sentence().split()[0],
            'id': i
        }
        for i in range(popular_accounts_num)]

    links = {}

    return render(
        request,
        'index.html',
        {
            'data':
                {
                    'account':
                        {
                            "login": "kdanil01",
                            'avatar': 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1',
                        },
                    'questions': questions_list,
                    'popular_tags': popular_tags,
                    'popular_accounts': popular_accounts,
                    'links': links,
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
                    'current_date': date.today(),
                    'id': question_id
                },
        }
    )


def get_login(request):
    return render(
        request,
        'login.html',
        {
            'login': "coolguy64"
        }
    )


def sign_up(request):
    return render(
        request,
        'signup.html',
        {
            'login': "coolguy64"
        }
    )


def ask_question(request):
    return render(
        request,
        'ask.html',
        {
            'login': "coolguy64"
        }
    )
