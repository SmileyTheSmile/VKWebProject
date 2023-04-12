from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, F
import lorem

# python manage.py makemigrations
# python manage.py migrate

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
        return DummyInfo.popular_users(num)
    
    def register_user(**kwargs):
        user = User.objects.create_user(**kwargs)
        user.save()

    def popular_users_broken(num):
        return User.annotate(fieldsum=sum(F('vote__score'))).order_by('vote__score').get(num)
        
        
class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
        )
    nickname = models.CharField(
        max_length=256,
        default='lame_user',
        blank=False,
        )
    avatar = models.ImageField(
        default='default.jpg',  
        upload_to='profile_pics',
    )
    
    def __str__(self):
        return self.user.username
    
    def absolute_url(self):
        return f"/profile/{self.pk}/"
    
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
        to=Profile,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
        )
    title = models.CharField(
        max_length=256,
        blank=False,
        )
    date_published = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        )
    tags = models.ManyToManyField(
        to=Tag,
        )
    content = models.TextField(
        max_length=30000,
    )
    
class Answer(models.Model):
    author = models.OneToOneField(
        to=Profile,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        )
    is_correct = models.BooleanField(
        default=False,
        blank=False,
        )
    date_published = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        )
    content = models.TextField(
        blank=False,
        )

class Vote(models.Model):
    author = models.OneToOneField(
        to=Profile,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        )
    score = models.IntegerField(
        choices=[(-1, 'dislike'), (1, 'like')],
        blank=False,
        )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
    
class AnswerVote(Vote):
    question = models.ForeignKey(
        to=Answer,
        blank=False,
        on_delete=models.CASCADE,
        )

class QuestionVote(Vote):
    question = models.ForeignKey(
        to=Question,
        blank=False,
        on_delete=models.CASCADE,
        )