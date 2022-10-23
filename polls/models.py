from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Test(models.Model):
    testtype = models.CharField(max_length=100)
    level = models.CharField(max_length=40)
    pub_date = models.DateTimeField('date published')
    maxballs = models.IntegerField(null=False)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Question(models.Model):
    testnumb = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    answer = models.BooleanField(verbose_name = 'Правильный ответ')

    def __str__(self):
        return self.choice_text


class ResultTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    balls = models.IntegerField(default=0)


# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     bio = models.TextField(null=True, blank=True)
#     profile_pic = models.ImageField(null=True, blank=True, upload_to="profile/images/")
#     instagram = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.user)
