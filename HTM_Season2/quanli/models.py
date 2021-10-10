from django.db import models
from userprofile.models import MyUser


# Create your models here.


# Model manager
class DiemThiSinhManager(models.Manager):
    """
    Custom manager to provide high-level API for model
    """
    def getAllScore(self):
        """
        Method to get all the current scores
        Return:
            A Query set of contestants and their scores
        """

        thisinh_scores = []

        # Create new score if the score is empty
        for thisinh in MyUser.objects.filter(is_contestant=True):
            # The get_or_create method return a tuple (object, created)
            thisinh_scores.append(self.get_or_create(user=thisinh)[0])
        
        return thisinh_scores

    def updateScore(self, username, score):
        """
        Method to update the score of the given contestant

        Params:
            
            username: The username of the user in database (not display name)
            score: The new score

        """
        user = MyUser.objects.get(username=username)
        currentScoreRecord = self.get(user=user)
        
        # Update score
        currentScoreRecord.score = score
        currentScoreRecord.save()


# Model
class DiemThiSinh(models.Model):
    """
    Model for managing contestants' score
    """
    # The contestant this model is linked to
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, verbose_name="Điểm thí sinh")

    objects = DiemThiSinhManager()

    def __str__(self):
        return ":".join([str(self.user), str(self.score)])
        
