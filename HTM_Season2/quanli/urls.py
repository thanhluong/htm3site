from django.urls import path
from django.views.generic import TemplateView

from .views import score, currentQuestion, updateRound
from .views import NewAnswer, httpSubmitAnswer
from .views import broadcastSignal
from .views import ringBell, resetRingingState
from .views import gianhQuyen, beginAcceptingGQ, stopAcceptingGQ, resetGQState
from .views import ngoiSaoHiVong, resetNSHVState
from .views import beginAcceptingAnswer, stopAcceptingAnswer, getDapAnThiSinh
from .views import gameState

urlpatterns = [
    # Handle grading requests
    path("score/", score, name="score"),
    path("score/<str:username>/<int:score>", score, name="updateScore"),
    path("currentQuestion/", currentQuestion, name="currentQuestion"),
    # Handle round updating
    path("updateRound/", updateRound, name="updateRound"),
    # Handle submiting answer
    path("answer/", NewAnswer.as_view(), name="answer"),
    path("httpSubmitAnswer/", httpSubmitAnswer, name="httpSubmitAnswer"),
    # Handle broadcast signal
    path("broadcastSignal/", broadcastSignal, name="broadcastSignal"),
    # Handle ringing request
    path("ringBell/", ringBell, name="ringBell"),
    path("resetRingingState/", resetRingingState, name="resetRingingState"),
    # Handle gianhQuyen request
    path("gianhQuyen/", gianhQuyen, name="gianhQuyen"),
    path("beginAcceptingGQ/", beginAcceptingGQ, name="beginAcceptingGQ"),
    path("stopAcceptingGQ/", stopAcceptingGQ, name="stopAcceptingGQ"),
    path("resetGQState/", resetGQState, name="resetGQState"),
    # Handle ngoiSaoHiVong request
    path("ngoiSaoHiVong/", ngoiSaoHiVong, name="ngoiSaoHiVong"),
    path("resetNSHVState/", resetNSHVState, name="resetNSHVState"),
    # Handle accepting new answer or stop accepting answer
    path("handleAcceptingAnswer/", beginAcceptingAnswer,
         name="handleAcceptingAnswer"),
    path("handleStopAcceptingAnswer/", stopAcceptingAnswer,
         name="handleStopAcceptingAnswer"),
    # Handle display dapan
    path("getDapAnThiSinh/", getDapAnThiSinh, name="getDapAnThiSinh"),
    # Handle game state
    path("gameState/", gameState, name="gameState"),
    path("viewGameState/", TemplateView.as_view(template_name="gameState.html"))
]
