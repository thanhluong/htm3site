from django.urls import path
from .forms import TangTocQuestionForm
from .views import NewQuestion, getAvailableFields, getNewQuestion

urlpatterns = [
    path("newQuestion/", NewQuestion.as_view(), name="newTangTocQuestion"),
    path("getField/", getAvailableFields, name="tangtoc"),
    path("tangtocQuestions/<str:field>", getNewQuestion, name="tangtocQuestions"),
]
