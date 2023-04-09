from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
        

class QuestionManager(models.Manager):
    def question_by_id():
        pass
    
    def questions_by_tag():
        pass
    
    def recent_questions(num):
        return DummyInfo.questions_list(num)
    
    def top_questions():
        pass
    
    def create_question():
        pass

class TagManager(models.Manager):
    def popular_tags(num):
        return DummyInfo.popular_tags(num)
    
    def random_tags():
        pass

class UserManager(models.Manager):
    def authenticate(username: str, password: str):
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            pass
        else:
            pass
    
    def popular_users(num):
        return DummyInfo.popular_tags(num)
    
    def register_user(**kwargs):
        user = User.objects.create_user(**kwargs)
        user.save()
        
        
class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
        )
    rating = models.IntegerField(default=0, blank=False)
    avatar = models.ImageField()
    
    def __str__(self):
        return self.user.string()
    
    def absolute_url(self):
        return f"/post/{self.pk}/"
    
    class Meta:
        db_table = 'profile'
        ordering = ['-user']
    
    
class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True
        )
    
    
class Question(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        )
    title = models.CharField(
        max_length=255,
        blank=False,
        )
    rating = models.IntegerField(
        default=0,
        blank=False,
        )
    date_published = models.DateTimeField(
        auto_now=True,
        blank=False,
        )
    tags = models.ManyToManyField(
        to=Tag,
        )
    content = models.TextField()
    
    
class Answer(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        )
    is_correct = models.BooleanField(
        default=False,
        blank=False,
        )
    rating = models.IntegerField(
        default=0,
        blank=False,
        )
    date_published = models.DateTimeField(
        auto_now=True,
        blank=False,
        )
    content = models.TextField(
        blank=False,
        )
