from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, F, Sum, Q
from django.db.models.signals import post_save
from django.dispatch import receiver

# python manage.py makemigrations HAsker
# python manage.py makemigrations
# python manage.py migrate

class IRateableManager(models.Manager):
    def update_rating(self):
        pass


class QuestionManager(IRateableManager):
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
        questions = self.annotate(total_score=Sum('votes__score'))
        for question in questions:
            question.rating = question.total_score or 0
        self.bulk_update(questions, ['rating'])   
    
    def update_answers_num(self):
        questions = self.annotate(answers_count=Count('answers'))
        for question in questions:
            question.rating = question.answers_count
        self.bulk_update(questions, ['answers_num'])    

class AnswerManager(IRateableManager):
    def update_rating(self):
        answers = self.annotate(total_score=Sum('votes__score'))
        for answer in answers:
            answer.rating = answer.total_score or 0
        self.bulk_update(answers, ['rating'])    

class ProfileManager(IRateableManager):
    def popular_users(self, num):
        return self.order_by('-rating', 'user__date_joined')[:num]
    
    def update_rating(self):
        profiles = self.annotate(total_score=Sum('answervote__score') + Sum('questionvote__score'))
        for profile in profiles:
            profile.rating = profile.total_score or 0
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
        blank=True,
        default='default_avatar.jpeg',  
        upload_to='avatars/%Y/%m/%d/',
    )

    def __str__(self):
        return self.user.username

    def absolute_url(self):
        return f"/profile/{self.pk}/"
    
    class Meta:
        db_table = 'profile'
        ordering = ['-user']
    
'''
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance,
            nickname=nickname,
            avatar=avatar,)
        instance.profile.save()
'''
    

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
    answers_num = models.IntegerField(
            blank=False,
            default=0,
        )


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