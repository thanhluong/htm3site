from django.forms import ModelForm
from .models import ChinhPhucQuestion, ChinhPhucAnswer

class ChinhPhucQuestionForm(ModelForm):
    """
    The form to create a new Khoi Dong question
    """

    class Meta:
        model = ChinhPhucQuestion
        fields = "__all__"

class ChinhPhucAnswerForm(ModelForm):
    """
    The form to create a new answer for Khoi Dong
    """

    class Meta:
        model = ChinhPhucAnswer
        exclude = ["question", "thisinh"]