from django.db import models
from user.models import User


class HousecleaningReservation(models.Model):
    USER = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    SERVICE_STARTING_TIME = models.ForeignKey('ServiceStartingTime', on_delete=models.SET_NULL, null=True)
    SERVICE_DURATION = models.ForeignKey('ServiceDuration', on_delete=models.SET_NULL, null=True)
    RESERVE_CYCLE = models.ForeignKey('ReserveCycle', on_delete=models.SET_NULL, null=True)
    STATUS = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    SERVICE_DAY_OF_WEEK_HOUSECLEANING_RESERVATION = models.ManyToManyField('ServiceDayOfWeek', through='HousecleaningReservation_ServiceDayOfWeek')
    service_start_date = models.DateField()
    reserve_location = models.CharField(max_length=300, null=True)
    have_pet = models.BooleanField(null=True)
    regist_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'HOUSECLEANING_RESERVATION'


class ServiceDuration_ServiceStartingTime(models.Model):
    SERVICE_DURATION = models.ForeignKey('ServiceDuration', on_delete=models.SET_NULL, null=True)
    SERVICE_STARTING_TIME = models.ForeignKey('ServiceStartingTime', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'SERVICE_DURATION_SERVICE_STATING_TIME'


class HousecleaningReservation_ServiceDayOfWeek(models.Model):
    HOUSECLEANING_RESERVATION = models.ForeignKey('HousecleaningReservation', on_delete=models.SET_NULL, null=True)
    SERVICE_DAY_OF_WEEK = models.ForeignKey('ServiceDayOfWeek', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'HOUSECLEANING_RESERVATION_SERVICE_DAY_OF_WEEK'


class ReserveCycle(models.Model):
    reserve_cycle = models.CharField(max_length=50)

    class Meta:
        db_table = 'RESERVE_CYCLE'


class ServiceDuration(models.Model):
    service_duration = models.CharField(max_length=50)

    class Meta:
        db_table = 'SERVICE_DURATION'


class ServiceStartingTime(models.Model):
    starting_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'SERVICE_STARTING_TIME'


class ServiceDayOfWeek(models.Model):
    service_day_of_week = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'SERVICE_DAY_OF_WEEK'


class Status(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'STATUS'
