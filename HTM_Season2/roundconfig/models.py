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
