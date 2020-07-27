from django.views import View
from django.http import JsonResponse
from user.utils import login_decorator

from user.models import User
from move.models import MoveReservation
from housecleaning.models import HousecleaningReservation


class UserProfileView(View):
    @login_decorator
    def get(self, request):
        user_profile = list(User.objects.filter(id=request.user.id).values())

        return JsonResponse({'User_Profile': user_profile}, status=200)


class HousecleaningReservationsView(View):
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
                dict_data['service_duration'] = result.SERVICE_DURATION.SRVC_DURATION
                dict_data['starting_time'] = result.SERVICE_STARTING_TIME.starting_time
                dict_data['service_start_date'] = result.service_start_date
                dict_data['reserve_location'] = result.reserve_location
                dict_data['have_pet'] = result.have_pet
                dict_data['status'] = result.STATUS.status

                hr_orders.append(dict_data)

            return JsonResponse({"hr_orders": hr_orders}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=401)


class MoveReservationsView(View):
    @login_decorator
    def get(self, request):
        move_user = MoveReservation.objects.select_related(
            'USER',
            'MOVE_CATEGORY').filter(USER_id=request.user.id).order_by('id')

        try:
            move_orders = list()

            for result in move_user:
                dict_data = dict()
                dict_data['id'] = result.id
                dict_data['name'] = result.USER.name
                dict_data['move_category'] = result.MOVE_CATEGORY.name
                dict_data['address'] = result.address
                dict_data['phone_number'] = result.mobile_number

                move_orders.append(dict_data)

            return JsonResponse({"move_orders": move_orders}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=401)
