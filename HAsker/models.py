from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, F, Sum, Q
import lorem

# python manage.py makemigrations HAsker
# python manage.py makemigrations
# python manage.py migrate


class QuestionManager(models.Manager):
    # TODO Add queries for differently sorted questions
    def question_by_id(self, id):
        return self.filter(id=id)
    
    def questions_by_tag(self, tag_id):
        return self.all().filter(tags__in=tag_id)
    
    def recent_questions(self):
        return self.all().order_by("date_published")
    
    def top_questions(self):
        return self.all().order_by("likes_count")
    
    def create_question(self):
        pass


class TagManager(models.Manager):
    def popular_tags(self, num):
        return self.annotate(
            question_count=Count('question')
            ).order_by('-question_count')[:num]
        #return DummyInfo.popular_tags(num)
    
    def random_tags():
        pass


class ProfileManager(models.Manager):
    def popular_users(self, num):
        return self.annotate(
                rating=Sum('questionvote__score') + Sum('answervote__score')
            ).order_by('-rating', '-user__date_joined')[:num]
        
# TODO https://github.com/ziontab/tp-tasks/blob/master/files/markdown/task-5.md
class Profile(models.Model):
    objects = ProfileManager()

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
        upload_to='profile_pics/%Y/%m/%d/',
    )
    
    def __str__(self):
        return self.user.username
    
    def absolute_url(self):
        return f"/profile/{self.pk}/"
    
    class Meta:
        db_table = 'profile'
        ordering = ['-user']
    

class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True
        )
    
#TODO Make a field for the total likes count so that the database doesn't have to count them each time

class Question(models.Model):
    objects = QuestionManager()

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

    @property
    def likes_count(self):
        return self.votes.aggregate(Sum('score'))['score__sum']


class Answer(models.Model):
    author = models.ForeignKey(
        to=Profile,
        blank=False,
        null=True,
        unique=False,
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
    question = models.ForeignKey(
        to=Question,
        blank=False,
        on_delete=models.CASCADE,
        related_name="answers",
        )

    @property
    def likes_count(self):
        return self.votes.aggregate(Sum('score'))['score__sum']


class Vote(models.Model):
    author = models.ForeignKey(
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
        null=True,
    )

    class Meta:
        abstract = True


class QuestionVote(Vote):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="votes",
        )
    
    class Meta:
        unique_together = ['author', 'question']
 

class AnswerVote(Vote):
    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        related_name="votes",
        )

    class Meta:
        unique_together = ['author', 'answer']