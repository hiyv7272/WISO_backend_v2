from django.db import models
from user.models import User


class MoveCategory(models.Model):
    MV_CTGRY_NAME = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'MOVE_CATEGORY'


class MoveReservation(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    MV_CTGRY = models.ForeignKey(MoveCategory, on_delete=models.CASCADE)
    MV_RV_ADDRESS = models.CharField(max_length=250, null=True)
    MV_RV_MOBILE_NUMBER = models.CharField(max_length=100, null=True)
    MV_RV_REGIST_DATETIME = models.DateTimeField(auto_now_add=True)
    MV_RV_UPDATE_DATETIME = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MOVE_RESERVATION'
