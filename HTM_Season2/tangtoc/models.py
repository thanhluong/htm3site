from django.db import models
from userprofile.models import MyUser

# Create your models here.


class TangTocQuestionField(models.Model):
    """
    Model for field in Tang Toc round
    """

    # Name of the field to store in database
    name = models.CharField(
        max_length=50, primary_key=True, verbose_name="Tên lĩnh vực")

    # Code to avoid problem with Vietnamese
    code = models.CharField(max_length=30, blank=False, verbose_name="Tên không dấu")

    # Keep track whether this field is used
    used = models.BooleanField(default=False, verbose_name="Đã sử dụng")

    def __str__(self):
        return self.name


class TangTocQuestion(models.Model):
    """
    Model for questions in Tang Toc round
    """
    # No need to create a question ID in this case, Django will generate a primary key for each question

    # The text content of the question
    questionText = models.TextField(
        blank=False, verbose_name="Nội dung câu hỏi")

    # The field of this question
    questionField = models.ForeignKey(TangTocQuestionField, on_delete=models.CASCADE,
                                      verbose_name="Lĩnh vực")

    # The answer for this question
    answer = models.CharField(
        max_length=255, blank=False, verbose_name="Đáp án")

    def __str__(self):
        return str(self.questionField) + ": " + self.questionText


# This round does not need to have Answer model because the contestant will answer directly to MC
