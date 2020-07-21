import jwt
import json
import bcrypt
import requests

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from wiso.settings import SECRET_KEY
from .models import User


def validate_input(data):

    if len(data['password']) < 8:
        return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

    if len(data['phone_number']) != 11:
        return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)

    if User.objects.filter(USR_EMAIL=data['email']).exists():
        return JsonResponse({'message': 'DUPLICATE_EMAIL'}, status=401)

    if User.objects.filter(USR_MOBILE_NUMBER=data['phone_number']).exists():
        return JsonResponse({'message': 'DUPLICATE_MOBLIE_NUMBER'}, status=401)

    return None


class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data['email'])
            validation = validate_input(data)

            if validation:
                return validation
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode()
            User(
                USR_EMAIL=data['email'],
                USR_PASSWORD=hashed_password,
                USR_MOBILE_NUMBER=data['phone_number']
            ).save()

            return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message': 'INVALID_EMAIL_SYNTAX'}, status=400)
        except TypeError:
            return JsonResponse({'message': 'FAILED_HASHED'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(USR_EMAIL=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.USR_PASSWORD.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'access_token': access_token.decode('utf-8')}, status=200)

            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class KakaologinView(View):
    def get(self, request):
        kakao_access_code = request.GET.get('code', None)
        url = 'https://kauth.kakao.com/oauth/token'
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {
            'grant_type': 'authorization_code',
            'client_id': '4499b173b6f76ea45ebdb3164ece38b7',
            'redirect_url': 'http://localhost:8000/',
            'code': kakao_access_code
        }

        kakao_token_response = requests.post(url, headers=headers, data=body)
        kakao_token = json.loads(kakao_token_response.text).get('kakao_token')
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            'Authorization': f"""Bearer {kakao_token}""",
            'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers=headers)
        return HttpResponse(f"""{kakao_response.text}""")

    def post(self, request):
        try:
            kakao_token = request.headers["Authorization"]
            headers = ({"Authorization": f"Bearer {kakao_token}"})
            url = "https://kapi.kakao.com/v1/user/me"
            response = requests.get(url, headers=headers)
            kakao_user = response.json()

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        if User.objects.filter(USR_KAKAO_ID=kakao_user["id"]).exists():
            user_id = User.objects.get(USR_KAKAO_ID=kakao_user["id"]).id
            print('user_id', user_id)
            access_token = jwt.encode({'id': user_id}, SECRET_KEY, algorithm="HS256")
            print('access_token', access_token)
            return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)

        else:
            newUser = User.objects.create(
                USR_KAKAO_ID=kakao_user["id"],
                # email       = kakao_user["properties"]["account_email"], 
                USR_NAME=kakao_user["properties"]["nickname"]
            )
            access_token = jwt.encode({'id': newUser.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)