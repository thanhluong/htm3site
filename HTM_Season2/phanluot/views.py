from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from .forms import PhanLuotQuestionForm
from .models import PhanLuotQuestion

# Create your views here.


class NewQuestion(generic.CreateView):
    """
    Class-based view to handle creating a new question
    Usig a class-based view will provides us a defautl error-handling
    """

    form_class = PhanLuotQuestionForm
    success_url = reverse_lazy("newPhanLuotQuestion")
    template_name = "baseForm.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.form_class()
            return render(request, template_name="baseForm.html",
                          context={"form": form})
        else:
            return render(request, template_name="home.html",
                          context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})


def toDict(question: PhanLuotQuestion):
    """
    Helper method to convert a question to JSON format
    """
    return dict(questionText=question.questionText, answer=question.answer)

@login_required
def getFirstQuestion(request):
    """
    Function to get all the questions for Phan Luot in the format for JSON array
    """
    if not request.user.is_staff:
        return render(request, template_name="home.html",
              context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

    questions = [toDict(question) for question in PhanLuotQuestion.objects.all().order_by("questionID")][0]

    return render(request, template_name="phanluot/phanluot.html", context=dict(questions=questions, questID=0))

@login_required
def getSecondQuestion(request):
    """
    Function to get all the questions for Phan Luot in the format for JSON array
    """
    if not request.user.is_staff:
        return render(request, template_name="home.html",
              context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

    questions = [toDict(question) for question in PhanLuotQuestion.objects.all().order_by("questionID")][1]

    return render(request, template_name="phanluot/phanluot.html", context=dict(questions=questions, questID=1))
