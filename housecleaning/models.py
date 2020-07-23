from django.db import models
from user.models import User


class HousecleaningReservation(models.Model):
    USER = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    SRVC_START_TIME = models.ForeignKey('ServiceStartTime', on_delete=models.SET_NULL, null=True)
    SRVC_DURATION = models.ForeignKey('ServiceDuration', on_delete=models.SET_NULL, null=True)
    RESVE_CYCLE = models.ForeignKey('ReserveCycle', on_delete=models.SET_NULL, null=True)
    SRVC_DAY_OF_WEEK_HC_RESERVATION = models.ManyToManyField('ServiceDayOfWeek', through='HousecleaningReservationServiceDayOfWeek')
    STATUS = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    SRVC_START_DATE = models.DateField()
    RESVE_LOCATION = models.CharField(max_length=300, null=True)
    HAVE_PET = models.BooleanField(null=True)
    HS_RESERVATION_REGIST_DATETIME = models.DateTimeField(auto_now_add=True)
    HS_RESERVATION_UPDATE_DATETIME = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'HOUSECLEANING_RESERVATION'


class ServiceDurationServiceStartTime(models.Model):
    SRVC_DURATION = models.ForeignKey('ServiceDuration', on_delete=models.SET_NULL, null=True)
    SRVC_START_TIME = models.ForeignKey('ServiceStartTime', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'SERVICE_DURATION_SERVICE_START_TIME'


class HousecleaningReservationServiceDayOfWeek(models.Model):
    HS_RESERVATION = models.ForeignKey('HousecleaningReservation', on_delete=models.SET_NULL, null=True)
    SRVC_DAY_OF_WEEK = models.ForeignKey('ServiceDayOfWeek', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'HOUSECLEANING_RESERVATION_SERVICE_DAY_OF_WEEK'


class ReserveCycle(models.Model):
    RESVE_CYCLE = models.CharField(max_length=50)

    class Meta:
        db_table = 'RESERVE_CYCLE'


class ServiceDuration(models.Model):
    SRVC_DURATION = models.CharField(max_length=50)

    class Meta:
        db_table = 'SERVICE_DURATION'


class ServiceStartTime(models.Model):
    SRVC_START_TIME = models.CharField(max_length=50)

    class Meta:
        db_table = 'SERVICE_START_TIME'


class ServiceDayOfWeek(models.Model):
    SRVC_DAY_OF_WEEK = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'SERVICE_DAY_OF_WEEK'


class Status(models.Model):
    STATUS = models.CharField(max_length=50)

    class Meta:
        db_table = 'STATUS'
