from django.shortcuts import render
from .models import QuestionSetConfig

# Create your views here.


def getQuestionSetId():
    return QuestionSetConfig.objects.all().first().questionSetId
