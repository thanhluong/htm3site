from django.forms import ModelForm
from .models import KhoiDongQuestion, KhoiDongAnswer

class KhoiDongQuestionForm(ModelForm):
    """
    The form to create a new Khoi Dong question
    """

    class Meta:
        model = KhoiDongQuestion
        fields = "__all__"

class KhoiDongAnswerForm(ModelForm):
    """
    The form to create a new answer for Khoi Dong
    """

    class Meta:
        model = KhoiDongAnswer
        exclude = ["question", "thisinh"]