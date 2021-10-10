from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import NewQuestion, getQuestions

urlpatterns = [
    path("", getQuestions, name="vuotsong"),
    path("newQuestion/", NewQuestion.as_view(), name="newVuotSongQuestion"),
]