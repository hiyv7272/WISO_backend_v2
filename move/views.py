import json

from django.http import JsonResponse
from django.views import View
from user.utils import login_decorator, sms_service

from move.models import MoveReservation, MoveCategory
from user.models import User


class MoveReserve(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)

        if int(data['move_category_id']) > 3:
            return JsonResponse({'message': 'please choose between three options'})
        if len(data['mobile_number']) != 11:
            return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)

        try:
            MoveReservation(
                USER_id=request.user.id,
                MOVE_CATEGORY_id=data['move_category_id'],
                address=data['address'],
                mobile_number=data['mobile_number'],
            ).save()

            sms_service(data)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except TypeError:
            return JsonResponse({'message': 'FAILED_HASHED'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)

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


class MoveCategoryInfo(View):
    def get(self, request):
        move_categories = list(MoveCategory.objects.values())

        return JsonResponse({'move_categories': move_categories}, status=200)
