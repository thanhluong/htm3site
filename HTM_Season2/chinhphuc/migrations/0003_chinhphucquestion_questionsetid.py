# Generated by Django 2.2.8 on 2021-10-12 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinhphuc', '0002_auto_20190829_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinhphucquestion',
            name='questionSetID',
            field=models.IntegerField(default=1, verbose_name='Bộ câu hỏi'),
        ),
    ]
