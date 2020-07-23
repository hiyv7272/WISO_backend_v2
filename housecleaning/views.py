import json
import requests

from django.views import View
from django.http import JsonResponse
from my_settings import SMS_AUTH_ID, SMS_SERVICE_SECRET, SMS_FROM_NUMBER, SMS_URL
from user.utils import login_decorator
from user.models import User
from .models import (
    HousecleaningReservation,
    ReserveCycle,
    ServiceDuration,
    ServiceStartTime,
    ServiceDayOfWeek,
)


def sms_service(data, user):
    phone_number = user.phone_number
    address = data['reserve_location']

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-auth-key': f'{SMS_AUTH_ID}',
        'x-ncp-service-secret': f'{SMS_SERVICE_SECRET}',
    }
    data = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': f'{SMS_FROM_NUMBER}',
        'to': [
            f'{phone_number}',
        ],
        'subject': 'WISO-PROJECT',
        'content': f'가사도우미예약 완료되었습니다 ^^ 주소지 : {address}'
    }
    requests.post(SMS_URL, headers=headers, json=data)


class ReserveCycleView(View):
    def get(self, request):
        try:
            reserve_cycles = list(ReserveCycle.objects.values())

            return JsonResponse({'ReserverCycle': reserve_cycles}, status=200)
        except reserve_cycles.DoesNotExist:
            return JsonResponse({'message': 'INVALID_URL'}, status=404)


class ServiceDurationsView(View):
    def get(self, request):
        try:
            service_durations = list(ServiceDuration.objects.values())

            return JsonResponse({'ServiceDurations': service_durations}, status=200)
        except service_durations.DoesNotExist:
            return JsonResponse({'message': 'INVALID_URL'}, status=404)


class ServiceStartingTimesView(View):
    def get(self, request):
        try:
            service_starti_times = list(ServiceStartTime.objects.values())

            return JsonResponse({'ServiceStartingTimes': service_starti_times}, status=200)
        except service_starti_times.DoesNotExist:
            return JsonResponse({'message': 'INVALID_URL'}, status=404)


class ServiceDayOfWeeksView(View):
    def get(self, request):
        try:
            service_day_of_weeks = list(ServiceDayOfWeek.objects.values())

            return JsonResponse({'ServiceDayOfWeeks': service_day_of_weeks}, status=200)
        except service_day_of_weeks.DoesNotExist:
            return JsonResponse({'message': 'INVALID_URL'}, status=404)


class OnetimeReservateView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)

        try:
            HousecleaningReservation(
                USER_id=user.id,
                STATUS_id=data['status_id'],
                SRVC_START_TIME_id=data['starting_time_id'],
                SRVC_DURATION_id=data['service_duration_id'],
                RESVE_CYCLE_id=data['reserve_cycle_id'],
                SRVC_START_DATE=data['service_start_date'],
                RESVE_LOCATION=data['reserve_location'],
                HAVE_PET=data.get('have_pet', 0) == 1
            ).save()

            self.sms_service(data, user)
            return JsonResponse({'message': 'success'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
        except ReserveCycle.DoesNotExist:
            return JsonResponse({'message': 'reserve_cycle_id INVALID_VALUES'}, status=401)
        except ServiceDuration.DoesNotExist:
            return JsonResponse({'message': 'service_duration_id INVALID_VALUES'}, status=401)
        except ServiceStartTime.DoesNotExist:
            return JsonResponse({'message': 'starting_time_id INVALID_VALUES'}, status=401)
