from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy

from .models import DiemThiSinh

from khoidong.models import KhoiDongQuestion, KhoiDongAnswer
from vuotsong.models import VuotSongQuestion, VuotSongAnswer
from phanluot.models import PhanLuotQuestion, PhanLuotAnswer
from tangtoc.models import TangTocQuestion
from chinhphuc.models import ChinhPhucQuestion, ChinhPhucAnswer
from userprofile.models import MyUser

from khoidong.forms import KhoiDongAnswerForm
from vuotsong.forms import VuotSongAnswerForm
from chinhphuc.forms import ChinhPhucAnswerForm
from phanluot.forms import PhanLuotAnswerForm

import json

currentQuestionContent = ""
currentQuestionID = 0
currentRound = "khoidong"

acceptingAnswer = False

acceptingGQ = False
gianhQuyenUser = ""

# TODO: Add form classes for other rounds here
FORM_CLASSES = {
                "khoidong": KhoiDongAnswerForm,
                "vuotsong": VuotSongAnswerForm,
                "chinhphuc": ChinhPhucAnswerForm,
                "phanluot": PhanLuotAnswerForm
                }

currentRinger = ""
allRingers = []

currentNSHVer = ""
allNSHVers = []

# Create your views here.
@login_required
def score(request, username=None, score=None):
    """
    Function to handle the request to grading page

    Accepted methods:
        GET: Get the information of current grading, available to all users
        If username and score is provided, attempt to change the info in database
    Params:
        username: username of the contestant to be updated
        score: new score
    """

    diemThiSinhManager = DiemThiSinh.objects

    if request.method == "GET":
        if username is None:
            # This request is for grading info
            scores = diemThiSinhManager.getAllScore()
            userlist = []
            for score in scores:
                print("***", score.user.profile_pic)
                userlist.append({"score": score.score, "user": score.user, "avatar": score.user.profile_pic})
            return render(request, template_name="quanli/score.html", context={"scores": scores, "userlist": userlist, "footerDisplay": True})
        else:
            # This request is for updating
            if request.user.is_staff:
                diemThiSinhManager.updateScore(username, score)
                return HttpResponse("Success!")
            else:
                # This user is not allowed to do the update
                return HttpResponse("Not allowed to access")


class NewAnswer(generic.CreateView):
    """
    Class-based view to submit a new answer to the database
    """
    global currentQuestionID, currentRound, FORM_CLASSES, acceptingAnswer

    form_class = FORM_CLASSES[currentRound]
    success_url = reverse_lazy("answer")
    template_name = "baseForm.html"

    # Handle the post method to inlcude question number and
    def post(self, request):
        if currentRound not in ["vuotsong", "khoidong", "chinhphuc", "phanluot"]:
            return HttpResponseRedirect(reverse_lazy("answer"))

        # If currently no question is being presented, prevent thi sinh to submit answer
        # Also prevent thi sinh to submit answer if time out
        if currentQuestionID > 0 and acceptingAnswer:
            print("========> {}".format(acceptingAnswer))
            self.form_class = FORM_CLASSES[currentRound]

            user = request.user
            # Get the form data submitted by user
            formAnswer = self.form_class(request.POST)
            # Create an answer instance but not yet saved
            answer = formAnswer.save(commit=False)
            answer.thisinh = user

            # Find the correct round
            # Only these 2 rounds require submission to server
            if currentRound == "khoidong":
                answer.question = KhoiDongQuestion.objects.get(questionID=currentQuestionID)
            elif currentRound == "vuotsong":
                answer.question = VuotSongQuestion.objects.get(questionID=currentQuestionID)
            elif currentRound == "chinhphuc":
                answer.question = ChinhPhucQuestion.objects.get(questionID=currentQuestionID)
            elif currentRound == "phanluot":
                answer.question = PhanLuotQuestion.objects.get(questionID=currentQuestionID)
        
            # Save the answer
            answer.save()

        # Return a new page for the next question
        form = self.form_class()
        return render(request, template_name=self.template_name, context={"form": form, "answerView": True, "currentRound": currentRound})

    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={"form": form, "answerView": True, "currentRound": currentRound})

@login_required
def updateRound(request):
    global currentRound

    if request.method == "POST":
        if not request.user.is_staff:
            return HttpResponseForbidden()
        dataPost = request.POST
        # Update currentRound
        currentRound = dataPost.get("roundName")
        return HttpResponse("currentRound updated!")
    return HttpResponseForbidden()

def currentQuestion(request):
    """
    Function to handle the request for retrieve or updating current question

    Accepted methods:
        GET: Return the current question content in JSON format
        POST: Update the current question content
    """ 
    global currentQuestionContent, currentQuestionID, currentRound, acceptingAnswer

    if request.method == "GET":
        # Get the current question
        if currentRound == "khoidong":
            question = KhoiDongQuestion.objects.get(questionID=currentQuestionID)
        elif currentRound == "vuotsong":
            question = VuotSongQuestion.objects.get(questionID=currentQuestionID)
        elif currentRound == "chinhphuc":
            question = ChinhPhucQuestion.objects.get(questionID=currentQuestionID) 
        elif currentRound == "phanluot":
            question = PhanLuotQuestion.objects.get(questionID=currentQuestionID)

        # Get all answers for this question
        if currentRound == "khoidong":
            lastAnswer = KhoiDongAnswer.objects.filter(question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "vuotsong":
            lastAnswer = VuotSongAnswer.objects.filter(question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "chinhphuc":
            lastAnswer = ChinhPhucAnswer.objects.filter(question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "phanluot":
            lastAnswer = PhanLuotAnswer.objects.filter(question=question).filter(thisinh=request.user).order_by("-id")

        # print("***", question.values("questionText"))
        # for myiter in lastAnswer.values("answer"):
        #     print("###", myiter)
        lastAnswer = lastAnswer.values("answer")

        if len(lastAnswer) > 0:
            lastAnswer = lastAnswer[0]["answer"]
            return JsonResponse(json.dumps(dict(question=currentQuestionContent, answer=lastAnswer)), safe=False)
        return JsonResponse(json.dumps(dict(question=currentQuestionContent)), safe=False)
    
    elif request.method == "POST":
        if request.user.is_staff:
            dataPost = request.POST
            
            # Update the data for server to know about current question info
            currentQuestionContent = dataPost.get("question")
            currentQuestionID = int(dataPost.get("questionID"))
            currentRound = dataPost.get("round")

            return HttpResponse("Updated!")
        else:
            return HttpResponseForbidden()

@login_required
def ringBell(request):
    """
    Function to handle the request for retrieve or updating current ringer

    Accepted methods:
        GET: Return the current ringer name in JSON format
        POST: Update the current ringer name
    """ 
    global currentRinger
    global allRingers

    if request.method == "GET":
        # The person is already ringed
        if str(request.user) in allRingers:
            result = {"ringerName": "luong"}
            return JsonResponse(json.dumps(result), safe=False)
        # Return currentRinger
        result = {"ringerName": currentRinger}
        return JsonResponse(json.dumps(result), safe=False)
    elif request.method == "POST":
        # Another person ringed
        if len(currentRinger) > 0:
            return HttpResponseForbidden()
        # The person is already ringed
        if str(request.user) in allRingers:
            return HttpResponseForbidden()
        # Update currentRinger
        currentRinger = str(request.user)
        allRingers.append(currentRinger)
        print(currentRinger, "ringed a bell!")
        return HttpResponse("Ringed!")

@login_required
def resetRingingState(request):
    """
    Function to reset the state of the bell
    """ 
    global currentRinger

    # Only POST method is allowed
    if request.method != "POST":
        return HttpResponseForbidden()

    if request.user.is_staff:
        # Reset by assigning currentRinger to be an empty string
        currentRinger = ""
        return HttpResponse("Already reset!")
    else:
        return HttpResponseForbidden()

@login_required
def ngoiSaoHiVong(request):
    global currentNSHVer
    global allNSHVers

    if request.method == "GET":
        # The person is already ringed
        if str(request.user) in allNSHVers:
            result = {"ringerName": "luong"}
            return JsonResponse(json.dumps(result), safe=False)
        # Return currentRinger
        result = {"ringerName": currentNSHVer}
        return JsonResponse(json.dumps(result), safe=False)
    elif request.method == "POST":
        # Another person ringed
        if len(currentNSHVer) > 0:
            return HttpResponseForbidden()
        # The person is already ringed
        if str(request.user) in allNSHVers:
            return HttpResponseForbidden()
        # Update currentNSHVer
        currentNSHVer = str(request.user)
        allNSHVers.append(currentNSHVer)
        print(currentRinger, " da chon NSHV!")
        return HttpResponse("Ngoi sao hi vong!")

@login_required
def resetNSHVState(request):
    """
    Function to reset the state of the bell
    """ 
    global currentNSHVer

    # Only POST method is allowed
    if request.method != "POST":
        return HttpResponseForbidden()

    if request.user.is_staff:
        # Reset by assigning currentRinger to be an empty string
        currentNSHVer = ""
        return HttpResponse("Already reset!")
    else:
        return HttpResponseForbidden()

@login_required
def beginOrStopAcceptingAnswer(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    global acceptingAnswer

    if request.user.is_staff:
        acceptingAnswer = not acceptingAnswer
    
    return HttpResponse("Success")

@login_required
def beginAcceptingGQ(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    global acceptingGQ

    if request.user.is_staff:
        acceptingGQ = True
    
    return HttpResponse("Success")

@login_required
def stopAcceptingGQ(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    global acceptingGQ

    if request.user.is_staff:
        acceptingGQ = False
    
    return HttpResponse("Success")

@login_required
def resetGQState(request):
    global gianhQuyenUser

    if request.user.is_staff:
        gianhQuyenUser = ""

    return HttpResponse("Success")

@login_required
def gianhQuyen(request):
    global acceptingGQ, gianhQuyenUser
    
    if request.method == "GET":
        result = {"gianhQuyenUser": gianhQuyenUser,
                    "acceptingGQ": acceptingGQ}
        print(result)
        return JsonResponse(json.dumps(result), safe=False)
    elif request.method == "POST":
        if not acceptingGQ:
            return HttpResponseForbidden()
        if gianhQuyenUser == "":
            gianhQuyenUser = str(request.user)
            print(gianhQuyenUser, "gianh quyen tra loi!")
        return HttpResponse("Success") 

    return HttpResponseForbidden()    

@login_required
def getDapAnThiSinh(request):
    """
    The function to handle getting all the latest answers from thi sinh
    """

    global currentQuestionID, currentRound

    # Get the current question
    if currentRound == "khoidong":
        question = KhoiDongQuestion.objects.get(questionID=currentQuestionID)
    elif currentRound == "vuotsong":
        question = VuotSongQuestion.objects.get(questionID=currentQuestionID)
    else:
        question = PhanLuotQuestion.objects.get(questionID=currentQuestionID)

    # Get all answers for this question
    if currentRound == "khoidong":
        answers = KhoiDongAnswer.objects.filter(question=question).order_by("id")
    elif currentRound == "vuotsong":
        answers = VuotSongAnswer.objects.filter(question=question).order_by("id")
    else:
        answers = PhanLuotAnswer.objects.filter(question=question).order_by("id")

    # Get all the id of thisinh that submit the answer
    # thisinh_id = set([thisinh["thisinh"] for thisinh in answers.values("thisinh")])
    
    cnt = 1
    last_time = {}
    for thisinh in answers.values("thisinh"):
        last_time[ thisinh["thisinh"] ] = cnt
        cnt += 1
    print("***", last_time)
    thisinh_id = sorted(last_time, key=last_time.get)
    
    # Go through the answers and only retrieve the final answer of each
    final_answers = []
    for id in thisinh_id:
        last_answer = answers.filter(thisinh=id).last()
        final_answers.append(dict(
            thisinh=str(MyUser.objects.get(pk=id)),
            answer=last_answer.answer,
        ))

    return JsonResponse(json.dumps(final_answers), safe=False)
