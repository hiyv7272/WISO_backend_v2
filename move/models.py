from django.db import models
from user.models import User


class MoveCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'MOVE_CATEGORY'


class MoveReservation(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    MOVE_CATEGORY = models.ForeignKey(MoveCategory, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True)
    mobile_number = models.CharField(max_length=100, null=True)
    regist_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MOVE_RESERVATION'
