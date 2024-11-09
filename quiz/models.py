from django.db import models
from account.models import User


class Catalog(models.Model):
    name = models.CharField(max_length=100)


class Test(models.Model):
    title = models.CharField(max_length=100)
    catalog = models.ForeignKey(Catalog, related_name='tests', on_delete=models.CASCADE)


class Question(models.Model):
    text = models.CharField(max_length=255)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)


class Choice(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)


class TestResults(models.Model):
    test = models.ForeignKey(Test, related_name='test_results', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='test_results', on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    result_percentage = models.FloatField()
