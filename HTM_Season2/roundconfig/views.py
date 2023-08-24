from django.shortcuts import render
from .models import QuestionSetConfig
from .models import QuestionConfig
from .models import RoundState

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


def getRoundState():
    roundStateObject = RoundState.objects.all().first()
    return {
        "acceptingAnswer": roundStateObject.acceptingAnswer,
        "acceptingGQ": roundStateObject.acceptingGQ,
        "gianhQuyenUser": roundStateObject.gianhQuyenUser,
        "currentRinger": roundStateObject.currentRinger,
        "currentNSHVer": roundStateObject.currentNSHVer,
    }


def setAcceptingAnswer(acceptingAnswer):
    roundStateObject = RoundState.objects.all().first()
    roundStateObject.acceptingAnswer = acceptingAnswer
    roundStateObject.save()


def setAcceptingGQ(accpetingGQ):
    roundStateObject = RoundState.objects.all().first()
    roundStateObject.acceptingGQ = accpetingGQ
    roundStateObject.save()


def setGianhQuyenUser(gianhQuyenUser):
    roundStateObject = RoundState.objects.all().first()
    roundStateObject.gianhQuyenUser = gianhQuyenUser
    roundStateObject.save()


def setCurrentNSHVer(currentNSHVer):
    roundStateObject = RoundState.objects.all().first()
    roundStateObject.currentNSHVer = currentNSHVer
    roundStateObject.save()


def setCurrentRinger(currentRinger):
    roundStateObject = RoundState.objects.all().first()
    roundStateObject.currentRinger = currentRinger
    roundStateObject.save()
