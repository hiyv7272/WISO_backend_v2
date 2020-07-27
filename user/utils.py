import jwt
import requests

from django.http import JsonResponse
from wiso.settings import SECRET_KEY
from my_settings import SMS_AUTH_ID, SMS_SERVICE_SECRET, SMS_FROM_NUMBER, SMS_URL
from .models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            user = User.objects.get(id=payload["id"])
            request.user = user
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        except TypeError:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper


def sms_service(data):
    if data:
        mobile_number = data['mobile_number']
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
            f'{mobile_number}',
        ],
        'subject': 'WISO-PROJECT',
        'content': f'이사 문의 등록이 완료되었습니다 ^^ 주소지 : {address}'
    }

    requests.post(SMS_URL, headers=headers, json=data)
