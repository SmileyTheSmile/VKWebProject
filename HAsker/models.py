from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, F, Sum, Q
import lorem
import itertools

# python manage.py makemigrations HAsker
# python manage.py makemigrations
# python manage.py migrate

class IRateableManager(models.Manager):
    def update_rating(self):
        pass


class QuestionManager(IRateableManager):
    # TODO Add queries for differently sorted questions
    def question_by_id(self, id):
        return self.filter(id=id)
    
    def questions_by_tag(self, tag_id):
        return self.all().filter(tags__id=tag_id)
    
    def recent_questions(self):
        return self.all().order_by("-date_published")
    
    def top_questions(self):
        return self.all().order_by("-rating")
    
    def create_question(self):
        pass
    
    def update_rating(self):
        questions = self.all()
        for question in questions:
            question_votes = question.votes.values_list('score')
            question.rating = sum(itertools.chain(*question_votes)) or 0
            
        self.bulk_update(questions, ['rating'])    

class AnswerManager(IRateableManager):
    def update_rating(self):
        answers = self.all()
        for answer in answers:
            answer_votes = answer.votes.values_list('score')
            answer.rating = sum(itertools.chain(*answer_votes)) or 0
            
        self.bulk_update(answers, ['rating'])    

class ProfileManager(IRateableManager):
    def popular_users(self, num):
        return self.order_by('-rating', 'user__date_joined')[:num]
    
    def update_rating(self):
        profiles = self.all()
        for profile in profiles:
            answer_votes = profile.answervote_set.all()
            question_votes = profile.questionvote_set.all()
            total_score = answer_votes.aggregate(Sum('score'))['score__sum'] or 0
            total_score += question_votes.aggregate(Sum('score'))['score__sum'] or 0
            
            profile.rating = total_score
            
        self.bulk_update(profiles, ['rating'])
   
class TagManager(models.Manager):
    def popular_tags(self, num):
        return self.annotate(
            question_count=Count('question')
            ).order_by('-question_count')[:num]
        #return DummyInfo.popular_tags(num)
    
    def random_tags():
        pass


class IRateable(models.Model):
    rating = models.IntegerField(
            blank=False,
            default=0,
        )

    class Meta:
        abstract = True
        

# TODO https://github.com/ziontab/tp-tasks/blob/master/files/markdown/task-5.md
class Profile(IRateable):
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


class Question(IRateable):
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


    def update_votes_count(self):
        self.rating = self.votes.aggregate(Sum('score'))['score__sum']


class Answer(IRateable):
    objects = AnswerManager()
    
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
    
    
    def update_votes_count(self):
        self.rating = self.votes.aggregate(Sum('score'))['score__sum']


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
    object = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="votes",
        )
    
    class Meta:
        unique_together = ['author', 'object']
 

class AnswerVote(Vote):
    object = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        related_name="votes",
        )

    class Meta:
        unique_together = ['author', 'object']