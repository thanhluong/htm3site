from django.db import models

from userprofile.models import MyUser

# Get the directory of the MEDIA folder for this app


def questionDirectoryPath(instance, filename):
    """
    Method to return the path as MEDIA_ROOT/<username>/filename
    """
    return "chinhphuc/{}/{}".format(instance.questionID, filename)


class ChinhPhucQuestion(models.Model):
    """
    Model for question in Chinh Phuc round
    """

    # The question ID in in this round
    questionID = models.IntegerField(primary_key=True,
                                     verbose_name="Câu hỏi số")

    difficulty = models.CharField(max_length=10,
                                verbose_name="Độ khó",
                                choices = [("easy", "Dễ"), ("medium", "Trung bình"), ("hard", "Khó")],
                                blank=True)

    # The text content of the question
    questionText = models.TextField(blank=True,
                                    verbose_name="Nội dung câu hỏi")

    # The answer for this question
    answer = models.CharField(
        max_length=256, blank=False, verbose_name="Đáp án")

    # Question file (for video/sound/image questions)
    file = models.FileField(verbose_name="File đính kèm",
                            upload_to=questionDirectoryPath,
                            blank=True)

    fileType = models.CharField(max_length=10,
                                verbose_name="Loại file",
                                choices = [("sound", "Âm thanh"), ("video", "Video"), ("image", "Hình ảnh")],
                                blank=True)

    def __str__(self):
        return "Chinh phục: Câu hỏi {}".format(self.questionID)


class ChinhPhucAnswer(models.Model):
    """
    Model for the answer of constestant for Chinh Phuc round
    """

    # The question associated with this answer
    question = models.ForeignKey(to=ChinhPhucQuestion, on_delete=models.CASCADE)
    # The contestant associted with this answer
    thisinh = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)

    answer = models.CharField(max_length=500)

    def __str__(self):
        return "Câu hỏi số {}, thí sinh: {}: {}".format(self.question.questionID, 
                                                        self.thisinh, 
                                                        self.answer)
