from django.urls import path
from .views import NewQuestion
from .views import getFirstQuestion, getSecondQuestion

urlpatterns = [
    path("phanLuotButPha/", getFirstQuestion, name="phanLuotButPha"),
    path("phanLuotChinhPhuc/", getSecondQuestion, name="phanLuotChinhPhuc"),
    path("newQuestion/", NewQuestion.as_view(), name="newPhanLuotQuestion"),
]