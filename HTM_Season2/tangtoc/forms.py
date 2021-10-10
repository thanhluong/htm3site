from django.forms import ModelForm
from .models import TangTocQuestion

class TangTocQuestionForm(ModelForm):
    """
    Model form to create a new question for Tang Toc
    """

    class Meta:
        model = TangTocQuestion
        fields = "__all__"