from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import ChinhPhucQuestionForm
from .models import ChinhPhucQuestion

# Create your views here.

class NewQuestion(generic.CreateView):
    """
    Class-based view to handle creating a new question
    Usig a class-based view will provides us a defautl error-handling
    """

    form_class = ChinhPhucQuestionForm
    success_url = reverse_lazy("newChinhPhucQuestion")
    template_name = "baseForm.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = self.form_class()
            return render(request, template_name="baseForm.html",
                          context={"form": form})
        else:
            return render(request, template_name="home.html",
                          context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

def getFileType(fileName):
    """
    Helper fucntion to get the file type of the given file name
    """
    # +1 for the index to ignore the dot "."
    fileExtension = fileName[fileName.rindex(".")+1:].lower()
    if fileExtension in ["mp4", "mov", "avi"]:
        return "video"
    elif fileExtension in ["jpg", "png", "jpeg", "gif"]:
        return "image"
    else:
        return "sound"

def toDict(question: ChinhPhucQuestion):
    """
    Helper method to convert a question to JSON format
    """
    if question.file:
        return dict(questionID=question.questionID,
                    questionText=question.questionText,
                    file=question.file.url,
                    answer=question.answer,
                    difficulty=question.difficulty,
                    fileType=getFileType(question.file.url))
    else:
        return dict(questionID=question.questionID,
                    questionText=question.questionText, 
                    answer=question.answer,
                    difficulty=question.difficulty)

@login_required
def getQuestions(request):
    """
    Function to view all questions for Chinh Phuc round. Format: JSON
    """
    if not request.user.is_staff:
        return render(request, template_name="home.html",
              context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

    questions = [toDict(question) for question in ChinhPhucQuestion.objects.all().order_by("questionID")]
    return render(request, template_name="chinhphuc/chinhphuc.html", context=dict(questions=questions))