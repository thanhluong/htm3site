from django.forms import ModelForm
from .models import VuotSongQuestion, VuotSongAnswer

class VuotSongQuestionForm(ModelForm):
    """
    The form to create a new Khoi Dong question
    """

    class Meta:
        model = VuotSongQuestion
        fields = "__all__"

class VuotSongAnswerForm(ModelForm):
    """
    The form to create a new answer for Khoi Dong
    """

    class Meta:
        model = VuotSongAnswer
        exclude = ["question", "thisinh"]