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

from roundconfig.views import getCurrentRound, setCurrentRound
from roundconfig.views import getCurrentQuestion, setCurrentQuestion
from roundconfig.views import getRoundState
from roundconfig.views import setAcceptingAnswer
from roundconfig.views import setAcceptingGQ, setGianhQuyenUser
from roundconfig.views import setCurrentNSHVer, getAllNSHVers, addToAllNSHVers
from roundconfig.views import setCurrentRinger, getAllRingers, addToAllRingers
from roundconfig.views import getGameState, setGameState

from websocket import create_connection
from django.conf import settings

import json


# TODO: Add form classes for other rounds here
FORM_CLASSES = {
    "khoidong": KhoiDongAnswerForm,
    "vuotsong": VuotSongAnswerForm,
    "chinhphuc": ChinhPhucAnswerForm,
    "phanluot": PhanLuotAnswerForm
}

# allNSHVers = []

# Create your views here.


def sendWebSocketMessage(cmd, params):
    ws = create_connection("ws://%s:%d/" %
                           (settings.WS_HOSTNAME, settings.WS_PORT))
    wsMessage = {
        "secret_key": settings.WS_SECRET_KEY,
        "cmd": cmd,
        "params": params
    }
    ws.send(json.dumps(wsMessage))
    ws.close()


@login_required
def gameState(request):
    if request.method == "POST":
        # Update the game state (screenshot as base64)
        setGameState(request.POST.get("base64img"))
        return HttpResponse("Success!")
    elif request.method == "GET":
        # Get the game state
        return JsonResponse(json.dumps(dict(base64img=getGameState())), safe=False)


@login_required
def roundState(request):
    if request.method != "GET":
        return HttpResponseForbidden()
    return JsonResponse(json.dumps(getRoundState()), safe=False)


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
                userlist.append(
                    {"score": score.score, "user": score.user, "avatar": score.user.profile_pic})
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
    global FORM_CLASSES

    success_url = reverse_lazy("answer")
    template_name = "baseForm.html"

    # Handle the post method to include question number and
    def post(self, request):
        currentRound = getCurrentRound()

        if currentRound not in ["vuotsong", "khoidong", "chinhphuc", "phanluot"]:
            return HttpResponseRedirect(reverse_lazy("answer"))

        currentQuestionID = getCurrentQuestion()["currentQuestionID"]
        acceptingAnswer = getRoundState()["acceptingAnswer"]

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
                answer.question = KhoiDongQuestion.objects.get(
                    questionID=currentQuestionID)
            elif currentRound == "vuotsong":
                answer.question = VuotSongQuestion.objects.get(
                    questionID=currentQuestionID)
            elif currentRound == "chinhphuc":
                answer.question = ChinhPhucQuestion.objects.get(
                    questionID=currentQuestionID)
            elif currentRound == "phanluot":
                answer.question = PhanLuotQuestion.objects.get(
                    questionID=currentQuestionID)

            # Save the answer
            answer.save()

        # Return a new page for the next question
        form = self.form_class()

        return render(
            request,
            template_name=self.template_name,
            context={
                "form": form,
                "answerView": True,
                "currentRound": currentRound
            })

    def get(self, request):
        currentRound = getCurrentRound()
        form = FORM_CLASSES[currentRound]()
        return render(
            request,
            template_name=self.template_name,
            context={
                "form": form,
                "answerView": True,
                "currentRound": currentRound,
                "wsHost": settings.WS_HOSTNAME_FOR_CLIENT,
                "wsPort": settings.WS_PORT_FOR_CLIENT,
                "useWss": settings.WS_USE_WSS
            }
        )


@login_required
def httpSubmitAnswer(request):
    global FORM_CLASSES
    currentRound = getCurrentRound()

    if request.method != "POST":
        return HttpResponseForbidden()

    if currentRound not in ["vuotsong", "khoidong", "chinhphuc", "phanluot"]:
        return HttpResponseForbidden()

    form_class = FORM_CLASSES[currentRound]
    currentQuestionID = getCurrentQuestion()["currentQuestionID"]
    acceptingAnswer = getRoundState()["acceptingAnswer"]

    if currentQuestionID > 0 and acceptingAnswer:
        user = request.user
        answer = request.POST.get("answer")
        question = None

        # Find the correct round
        if currentRound == "khoidong":
            question = KhoiDongQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "vuotsong":
            question = VuotSongQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "chinhphuc":
            question = ChinhPhucQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "phanluot":
            question = PhanLuotQuestion.objects.get(
                questionID=currentQuestionID)

        formAnswer = form_class()

        userAnswer = formAnswer.save(commit=False)
        userAnswer.thisinh = user
        userAnswer.question = question
        userAnswer.answer = answer

        userAnswer.save()

    return HttpResponse("Success!")


@login_required
def updateRound(request):
    if request.method == "POST":
        if not request.user.is_staff:
            return HttpResponseForbidden()
        dataPost = request.POST
        # Update currentRound
        roundName = dataPost.get("roundName")
        setCurrentRound(roundName)
        return HttpResponse("currentRound updated!")

    return HttpResponseForbidden()


def currentQuestion(request):
    """
    Function to handle the request for retrieve or updating current question

    Accepted methods:
        GET: Return the current question content in JSON format
        POST: Update the current question content
    """
    currentRound = getCurrentRound()

    if request.method == "GET":
        # Get the current question
        currentQuestion = getCurrentQuestion()
        currentQuestionID = currentQuestion["currentQuestionID"]
        currentQuestionContent = currentQuestion["currentQuestionContent"]

        if currentRound == "khoidong":
            question = KhoiDongQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "vuotsong":
            question = VuotSongQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "chinhphuc":
            question = ChinhPhucQuestion.objects.get(
                questionID=currentQuestionID)
        elif currentRound == "phanluot":
            question = PhanLuotQuestion.objects.get(
                questionID=currentQuestionID)

        # Get all answers for this question
        if currentRound == "khoidong":
            lastAnswer = KhoiDongAnswer.objects.filter(
                question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "vuotsong":
            lastAnswer = VuotSongAnswer.objects.filter(
                question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "chinhphuc":
            lastAnswer = ChinhPhucAnswer.objects.filter(
                question=question).filter(thisinh=request.user).order_by("-id")
        elif currentRound == "phanluot":
            lastAnswer = PhanLuotAnswer.objects.filter(
                question=question).filter(thisinh=request.user).order_by("-id")

        # print("***", question.values("questionText"))
        # for myiter in lastAnswer.values("answer"):
        #     print("###", myiter)
        lastAnswer = lastAnswer.values("answer")

        if len(lastAnswer) > 0:
            lastAnswer = lastAnswer[0]["answer"]
            return JsonResponse(
                json.dumps(
                    dict(
                        question=currentQuestionContent,  # actually redundant
                        questionInfo=currentQuestion,
                        answer=lastAnswer
                    )
                ),
                safe=False)

        return JsonResponse(
            json.dumps(
                dict(
                    question=currentQuestionContent,  # actually redundant
                    questionInfo=currentQuestion
                )
            ),
            safe=False)

    elif request.method == "POST":
        if request.user.is_staff:
            dataPost = request.POST

            # Parse POST request
            currentQuestionContent = dataPost.get("question")
            currentQuestionID = int(dataPost.get("questionID"))
            currentQuestionFileType = dataPost.get("questionFileType")
            currentQuestionFile = dataPost.get("questionFile")

            # Update the data for server to know about current question info
            setCurrentQuestion(
                questionID=currentQuestionID,
                questionContent=currentQuestionContent,
                questionFileType=currentQuestionFileType,
                questionFile=currentQuestionFile
            )
            # currentRound = dataPost.get("round")

            # TODO: Send to WS proxy
            sendWebSocketMessage(
                cmd="updateQuestion",
                params={
                    "currentQuestionID": currentQuestionID,
                    "currentQuestionContent": currentQuestionContent,
                    "currentQuestionFileType": currentQuestionFileType,
                    "currentQuestionFile": currentQuestionFile,
                }
            )
            return HttpResponse("Updated!")
        else:
            return HttpResponseForbidden()


def broadcastSignal(request):
    """
    Function to handle the request for broadcast signal to all clients

    Accepted methods:
        POST: Broadcast the signal to all clients
    """
    if request.method != "POST":
        return HttpResponseForbidden()

    dataPost = request.POST
    cmd = dataPost.get("cmd")

    ws = create_connection("ws://%s:%d/" %
                           (settings.WS_HOSTNAME, settings.WS_PORT))
    wsMessage = {
        "secret_key": settings.WS_SECRET_KEY,
        "cmd": cmd,
        "params": {
            "status": "ok"
        }
    }
    ws.send(json.dumps(wsMessage))
    ws.close()
    return HttpResponse("Success!")


@login_required
def ringBell(request):
    """
    Function to handle the request for retrieve or updating current ringer

    Accepted methods:
        GET: Return the current ringer name in JSON format
        POST: Update the current ringer name
    """
    allRingers = getAllRingers()

    currentRinger = getRoundState()["currentRinger"]
    print("Got current ringer: ", currentRinger)
    print("All ringers: ", allRingers)

    if request.method == "GET":
        # The person is already ringed
        if str(request.user) in allRingers:
            result = {"ringerName": ""}
            return JsonResponse(json.dumps(result), safe=False)
        # Return currentRinger
        result = {"ringerName": currentRinger}
        print("Returning current ringer: ", result)
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
        setCurrentRinger(currentRinger)

        sendWebSocketMessage(cmd="ringBell", params={
                             "currentRinger": currentRinger})
        print(currentRinger, "ringed a bell!")
        return HttpResponse("Ringed!")


@login_required
def resetRingingState(request):
    """
    Function to reset the state of the bell
    """
    # Only POST method is allowed
    if request.method != "POST":
        return HttpResponseForbidden()

    if request.user.is_staff:
        # Reset by assigning currentRinger to be an empty string
        currentRinger = getRoundState()["currentRinger"]
        if len(currentRinger) > 0:
            addToAllRingers(currentRinger)  # marked as ringed
        setCurrentRinger("")
        sendWebSocketMessage(cmd="ringBell", params={"currentRinger": ""})
        return HttpResponse("Already reset!")
    else:
        return HttpResponseForbidden()


@login_required
def ngoiSaoHiVong(request):
    allNSHVers = getAllNSHVers()

    currentNSHVer = getRoundState()["currentNSHVer"]

    if request.method == "GET":
        # The person is already ringed
        if str(request.user) in allNSHVers:
            result = {"ringerName": ""}
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
        setCurrentNSHVer(currentNSHVer)

        sendWebSocketMessage(cmd="ngoiSaoHiVong", params={
                             "currentNSHVer": currentNSHVer})
        print(currentNSHVer, " da chon NSHV!")
        return HttpResponse("Ngoi sao hi vong!")


@login_required
def resetNSHVState(request):
    """
    Function to reset the state of the bell
    """
    # Only POST method is allowed
    if request.method != "POST":
        return HttpResponseForbidden()

    if request.user.is_staff:
        # Reset by assigning currentRinger to be an empty string
        currentNSHVer = getRoundState()["currentNSHVer"]
        if len(currentNSHVer) > 0:
            addToAllNSHVers(currentNSHVer)
        setCurrentNSHVer("")
        sendWebSocketMessage(cmd="resetNSHVState", params={"status": "ok"})
        return HttpResponse("Already reset!")
    else:
        return HttpResponseForbidden()


@login_required
def beginAcceptingAnswer(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    if request.user.is_staff:
        setAcceptingAnswer(True)
        sendWebSocketMessage(cmd="acceptAnswer", params={"status": True})

    return HttpResponse("Success")


@login_required
def stopAcceptingAnswer(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    if request.user.is_staff:
        setAcceptingAnswer(False)
        sendWebSocketMessage(cmd="acceptAnswer", params={"status": False})

    return HttpResponse("Success")


@login_required
def beginAcceptingGQ(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    if request.user.is_staff:
        setAcceptingGQ(True)
        sendWebSocketMessage(cmd="acceptGQ", params={"status": True})

    return HttpResponse("Success")


@login_required
def stopAcceptingGQ(request):
    """
    The fucntion to handle request of begin accepting answer from thi sinh
    """
    if request.user.is_staff:
        setAcceptingGQ(False)
        sendWebSocketMessage(cmd="acceptGQ", params={"status": False})

    return HttpResponse("Success")


@login_required
def resetGQState(request):
    if request.user.is_staff:
        setGianhQuyenUser("")
        sendWebSocketMessage(cmd="resetGQState", params={"status": "ok"})

    return HttpResponse("Success")


@login_required
def gianhQuyen(request):
    roundState = getRoundState()
    acceptingGQ = roundState["acceptingGQ"]
    gianhQuyenUser = roundState["gianhQuyenUser"]

    if request.method == "GET":
        result = {"gianhQuyenUser": gianhQuyenUser,
                  "acceptingGQ": acceptingGQ}
        print(result)
        return JsonResponse(json.dumps(result), safe=False)
    elif request.method == "POST":
        if not acceptingGQ:
            return HttpResponseForbidden()
        if gianhQuyenUser == "":
            setGianhQuyenUser(str(request.user))
            sendWebSocketMessage(
                cmd="gianhQuyen",
                params={
                    "gianhQuyenUser": str(request.user),
                    "acceptingGQ": acceptingGQ
                }
            )
            print(gianhQuyenUser, "gianh quyen tra loi!")
        return HttpResponse("Success")

    return HttpResponseForbidden()


@login_required
def getDapAnThiSinh(request):
    """
    The function to handle getting all the latest answers from thi sinh
    """
    currentRound = getCurrentRound()
    currentQuestionID = getCurrentQuestion()["currentQuestionID"]

    # Get the current question
    if currentRound == "khoidong":
        question = KhoiDongQuestion.objects.get(questionID=currentQuestionID)
    elif currentRound == "vuotsong":
        question = VuotSongQuestion.objects.get(questionID=currentQuestionID)
    else:
        question = PhanLuotQuestion.objects.get(questionID=currentQuestionID)

    # Get all answers for this question
    if currentRound == "khoidong":
        answers = KhoiDongAnswer.objects.filter(
            question=question).order_by("id")
    elif currentRound == "vuotsong":
        answers = VuotSongAnswer.objects.filter(
            question=question).order_by("id")
    else:
        answers = PhanLuotAnswer.objects.filter(
            question=question).order_by("id")

    # Get all the id of thisinh that submit the answer
    # thisinh_id = set([thisinh["thisinh"] for thisinh in answers.values("thisinh")])

    cnt = 1
    last_time = {}
    for thisinh in answers.values("thisinh"):
        last_time[thisinh["thisinh"]] = cnt
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
