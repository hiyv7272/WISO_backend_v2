from django.db import models


class User(models.Model):
    kakao_token = models.CharField(max_length=200, unique=True, null=True)
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=300)
    mobile_number = models.CharField(max_length=11, unique=True, null=True)
    regist_datetime = models.DateTimeField(null=True)
    update_datetime = models.DateTimeField(null=True)
    is_use = models.BooleanField(default=False)

    class Meta:
        db_table = 'USER'
