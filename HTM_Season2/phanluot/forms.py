from django.forms import ModelForm
from .models import PhanLuotQuestion, PhanLuotAnswer

class PhanLuotQuestionForm(ModelForm):
    """
    The form to create a new Phan Luot question
    """

    class Meta:
        model = PhanLuotQuestion
        fields = "__all__"

class PhanLuotAnswerForm(ModelForm):
    """
    The form to create a new answer for Phan Luot
    """

    class Meta:
        model = PhanLuotAnswer
        exclude = ["question", "thisinh"]