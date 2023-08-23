from django.db import models

# Create your models here.


class QuestionSetConfig(models.Model):
    ROUND_CHOICES = (
        ("khoidong", "Khởi động"),
        ("vuotsong", "Vượt sóng"),
        ("chinhphuc", "Chinh phục"),
        ("phanluot", "Phân lượt")
    )

    questionSetId = models.IntegerField(
        default=0,
        verbose_name="Mã bộ câu hỏi"
    )
    currentRound = models.CharField(
        max_length=16,
        choices=ROUND_CHOICES,
        default="khoidong",
        verbose_name="Vòng thi hiện tại"
    )


class QuestionConfig(models.Model):
    FILE_TYPE_CHOICES = (
        ("None", "Không có file"),
        ("audio", "Âm thanh"),
        ("video", "Video"),
        ("image", "Hình ảnh")
    )

    currentQuestionID = models.IntegerField(
        default=0,
        verbose_name="ID câu hỏi hiện tại"
    )
    currentQuestionContent = models.TextField(
        default="",
        verbose_name="Nội dung câu hỏi hiện tại"
    )
    currentQuestionFileType = models.CharField(
        max_length=16,
        choices=FILE_TYPE_CHOICES,
        default="None",
        verbose_name="Loại file đính kèm"
    )
    currentQuestionFile = models.TextField(
        default="",
        blank=True,
        verbose_name="Đường dẫn đính kèm"
    )
