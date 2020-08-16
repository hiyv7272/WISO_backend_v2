import json

from django.views import View
from django.http import JsonResponse
from user.utils import login_decorator, sms_service

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import (
    HousecleaningReservation,
    ReserveCycle,
    ServiceDuration,
    ServiceStartingTime,
    ServiceDayOfWeek,
)
from user.models import User
from .serializers import HouseCleanningReserveSerializer


class HouseCleanningOnetimeReserveView(viewsets.GenericViewSet):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        data['user_id'] = request.user.id
        query_set = HousecleaningReservation.objects.all()
        serializer = HouseCleanningReserveSerializer(query_set, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(validated_data=data)

        return Response(status=status.HTTP_200_OK)


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
            service_starti_times = list(ServiceStartingTime.objects.values())

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


class HousecleaningReserveInfo(View):
    @login_decorator
    def get(self, request):
        hr_user = HousecleaningReservation.objects.select_related(
            'USER',
            'SERVICE_STARTING_TIME',
            'SERVICE_DURATION',
            'RESERVE_CYCLE',
            'STATUS').filter(USER_id=request.user.id, STATUS_id=1).order_by('id')

        try:
            hr_orders = list()

            for result in hr_user:
                dict_data = dict()
                dict_data['id'] = result.id
                dict_data['name'] = result.USER.name
                dict_data['reserve_cycle'] = result.RESERVE_CYCLE.reserve_cycle
                dict_data['service_duration'] = result.SERVICE_DURATION.service_duration
                dict_data['starting_time'] = result.SERVICE_STARTING_TIME.starting_time
                dict_data['service_start_date'] = result.service_start_date
                dict_data['reserve_location'] = result.reserve_location
                dict_data['have_pet'] = result.have_pet
                dict_data['status'] = result.STATUS.status

                hr_orders.append(dict_data)

            return JsonResponse({"hr_orders": hr_orders}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=401)


class OnetimeReserve(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)

        try:
            HousecleaningReservation(
                USER_id=user.id,
                SERVICE_STARTING_TIME_id=data['service_starting_time_id'],
                SERVICE_DURATION_id=data['service_duration_id'],
                RESERVE_CYCLE_id=data['reserve_cycle_id'],
                STATUS_id=data['status_id'],
                service_start_date=data['service_start_date'],
                reserve_location=data['reserve_location'],
                have_pet=data.get('have_pet', 0) == 1
            ).save()

            user_data = dict()
            user_data['mobile_number'] = user.mobile_number
            user_data['address'] = data['reserve_location']
            sms_service(user_data)

            sms_service(user_data)

            return JsonResponse({'message': 'success'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
        except ReserveCycle.DoesNotExist:
            return JsonResponse({'message': 'reserve_cycle_id INVALID_VALUES'}, status=401)
        except ServiceDuration.DoesNotExist:
            return JsonResponse({'message': 'service_duration_id INVALID_VALUES'}, status=401)
        except ServiceStartingTime.DoesNotExist:
            return JsonResponse({'message': 'starting_time_id INVALID_VALUES'}, status=401)