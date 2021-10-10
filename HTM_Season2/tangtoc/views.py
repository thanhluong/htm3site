from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

from .forms import TangTocQuestionForm
from .models import TangTocQuestion, TangTocQuestionField

# Create your views here.


class NewQuestion(CreateView):
    """
    Class-based view to handle creating a new question
    Usig a class-based view will provides us a defautl error-handling
    """
    
    form_class = TangTocQuestionForm
    success_url = reverse_lazy("newTangTocQuestion")
    template_name = "baseForm.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.form_class()
            return render(request, template_name="baseForm.html",
                          context={"form": form})
        else:
            return render(request, template_name="home.html",
                          context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})


def getAvailableFields(request):
    """
    View to handle the request for get the current remaining available fields
    """

    # Check authentication
    if not request.user.is_staff:
        return render(request, template_name="home.html",
                    context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

    availableFields = []

    for field in TangTocQuestionField.objects.all():
        if not field.used:
            availableFields.append(field)
    
    return render(request, template_name="tangtoc/tangtocField.html", context={"fields": availableFields,
                                                               "numFields": range(len(availableFields))})


def toDict(question: TangTocQuestion):
    """
    Helper method to convert a question to JSON format
    """
    return dict(questionText=question.questionText, answer=question.answer)


@login_required
def getNewQuestion(request, field):
    """
    Function to handle request to get a new set of questions

    Params:
        fields (string): The field of the set of questions
    Return:
        questions (QuerySet): The set of question for this contestant
    """

    # Check authentication
    if not request.user.is_staff:
        return render(request, template_name="home.html",
                    context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

    # Check to see if this field is available
    field = TangTocQuestionField.objects.get(code=field)

    if field.used:
        return HttpResponseBadRequest("Bad request")

    # Get all questions of this query set
    questionsSets = TangTocQuestion.objects.filter(questionField=field)

    # Mark the field as unavailable
    field.used = True
    field.save()

    questions = [toDict(question) for question in questionsSets]

    return render(request, template_name="tangtoc/tangtoc.html", context=dict(questions=questions))
    
    
