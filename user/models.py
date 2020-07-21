from django.db import models


class User(models.Model):
    USR_KAKAO_ID = models.CharField(max_length=200, unique=True, null=True)
    USR_NAME = models.CharField(max_length=15)
    USR_EMAIL = models.CharField(max_length=200, unique=True)
    USR_PASSWORD = models.CharField(max_length=300)
    USR_MOBILE_NUMBER = models.CharField(max_length=11, unique=True, null=True)
    USR_REGIST_DATETIME = models.DateTimeField(auto_now_add=True)
    USR_UPDATE_DATETIME = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'USER'