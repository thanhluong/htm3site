from django.urls import path
from .views import NewQuestion, getQuestions

urlpatterns = [
    path("", getQuestions, name="khoidong"),
    path("newQuestion/", NewQuestion.as_view(), name="newKhoiDongQuestion"),
]