from django.db import models
from dataclasses import dataclass
import lorem

class DummyInfo:
    @staticmethod
    def questions_list(num: int):
        return  [
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
        for i in range(num)]

    @staticmethod
    def popular_tags(num: int):
        return [
        {
            'text': lorem.sentence().split()[0],
            'id': i
        }
        for i in range(num)]
        
    @staticmethod
    def popular_users(num: int):
        return [ 
        {
            'login': lorem.sentence().split()[0],
            'id': i
        }
        for i in range(num)]
        

@dataclass
class User:
    login: str
    email: str
    password: str
    nickname: str
    avatar: str
    registration_date: str
    rating: int
    
    
@dataclass
class Question:
    title: str
    description: str
    author: str
    creation_date: str
    tags: list
    rating: int
    
    
@dataclass
class Answer:
    content: str
    author: str
    creation_date: str
    is_correct: bool
    rating: int
    
    
@dataclass
class Tag:
    text: str