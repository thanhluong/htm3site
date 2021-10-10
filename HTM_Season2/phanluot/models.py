from django.db import models

from userprofile.models import MyUser

# Get the directory of the MEDIA folder for this app


def questionDirectoryPath(instance, filename):
    """
    Method to return the path as MEDIA_ROOT/<username>/filename
    """
    return "phanluot/{}/{}".format(instance.questionID, filename)


class PhanLuotQuestion(models.Model):
    """
    Model for question in Phan Luot round
    """

    # The question ID in in this round
    questionID = models.IntegerField(primary_key=True,
                                     verbose_name="Câu hỏi số")

    # The text content of the question
    questionText = models.TextField(blank=True,
                                    verbose_name="Nội dung câu hỏi")

    # The answer for this question
    answer = models.CharField(
        max_length=256, blank=False, verbose_name="Đáp án")

    def __str__(self):
        return "Phân lượt: Câu hỏi {}".format(self.questionID)


class PhanLuotAnswer(models.Model):
    """
    Model for the answer of constestant for Phan Luot round
    """

    # The question associated with this answer
    question = models.ForeignKey(to=PhanLuotQuestion, on_delete=models.CASCADE)
    # The contestant associted with this answer
    thisinh = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)

    answer = models.CharField(max_length=500)

    def __str__(self):
        return "Câu hỏi số {}, thí sinh: {}: {}".format(self.question.questionID, 
                                                        self.thisinh, 
                                                        self.answer)
