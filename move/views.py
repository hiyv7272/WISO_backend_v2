import json
import requests

from django.http import JsonResponse
from django.views import View
from my_settings import SMS_AUTH_ID, SMS_SERVICE_SECRET, SMS_FROM_NUMBER, SMS_URL
from user.utils import login_decorator
from move.models import MoveReservation, MoveCategory
from user.models import User


def sms_service(data):
    phone_number = data['phone_number']
    address = data['address']

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
        'content': f'이사 문의 등록이 완료되었습니다 ^^ 주소지 : {address}'
    }
    requests.post(SMS_URL, headers=headers, json=data)


class MoveReservate(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)

        if int(data['movecategory_id']) > 3:
            return JsonResponse({'message': 'please choose between three options'})
        if len(data['phone_number']) != 11:
            return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)
        try:
            MoveReservation(
                USER_id=user.id,
                MV_CTGRY_id=data['movecategory_id'],
                MV_RV_ADDRESS=data['address'],
                MV_RV_MOBILE_NUMBER=data['phone_number'],
            ).save()

            self.sms_service(data, user)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except TypeError:
            return JsonResponse({'message': 'FAILED_HASHED'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)


class MoveCategoryInfo(View):
    def get(self, request):
        move_categories = list(MoveCategory.objects.values())

        return JsonResponse({'move_categories': move_categories}, status=200)