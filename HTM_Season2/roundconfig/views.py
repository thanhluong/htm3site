from django.shortcuts import render
from .models import QuestionSetConfig
from .models import QuestionConfig

# Create your views here.


def getQuestionSetId():
    return QuestionSetConfig.objects.all().first().questionSetId


def getCurrentRound():
    return QuestionSetConfig.objects.all().first().currentRound


def setCurrentRound(roundName):
    configObject = QuestionSetConfig.objects.all().first()
    configObject.currentRound = roundName
    configObject.save()


def getCurrentQuestion():
    currentQuestionObject = QuestionConfig.objects.all().first()
    return {
        "currentQuestionID": currentQuestionObject.currentQuestionID,
        "currentQuestionContent": currentQuestionObject.currentQuestionContent,
        "currentQuestionFileType": currentQuestionObject.currentQuestionFileType,
        "currentQuestionFile": currentQuestionObject.currentQuestionFile
    }


def setCurrentQuestion(questionID, questionContent, questionFileType, questionFile):
    currentQuestionObject = QuestionConfig.objects.all().first()
    currentQuestionObject.currentQuestionID = questionID
    currentQuestionObject.currentQuestionContent = questionContent
    currentQuestionObject.currentQuestionFileType = questionFileType
    currentQuestionObject.currentQuestionFile = questionFile
    currentQuestionObject.save()
