from django.views import View
from django.http import JsonResponse
from user.utils import login_decorator
from housecleaning.models import HousecleaningReservation
from move.models import MoveReservation
from user.models import User


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
            'SRVC_START_TIME',
            'SRVC_DURATION',
            'RESVE_CYCLE',
            'STATUS').filter(USER_id=request.user.id, STATUS_id=1).order_by('id')
        try:
            hr_orders = [{
                'id': result.id,
                'name': result.USER.USR_NAME,
                'reserve_cycle': result.RESVE_CYCLE.RESVE_CYCLE,
                'service_duration': result.SRVC_DURATION.SRVC_DURATION,
                'starting_time': result.SRVC_START_TIME.SRVC_START_TIME,
                'service_start_date': result.SRVC_START_DATE,
                'reserve_location': result.RESVE_LOCATION,
                'have_pet': result.HAVE_PET,
                'status': result.STATUS.STATUS
                } for result in hr_user]
            
            return JsonResponse({"hr_orders": hr_orders}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"},status=401)


class MoveReservationsView(View):
    @login_decorator
    def get(self, request):
        move_user = MoveReservation.objects.select_related(
            'USER',
            'MV_CTGRY').filter(USER_id=request.user.id).order_by('id')
        try:
            move_orders = [{
                'id': result.id,
                'name': result.USER.USR_NAME,
                'movecategory': result.MV_CTGRY.MV_CTGRY_NAME,
                'address': result.MV_RV_ADDRESS,
                'phone_number': result.MV_RV_MOBILE_NUMBER
                } for result in move_user]
            
            return JsonResponse({"move_orders": move_orders}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"},status=401)