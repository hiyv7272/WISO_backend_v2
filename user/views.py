import jwt
import json
import bcrypt
import requests

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from wiso.settings import SECRET_KEY
from user.utils import login_decorator

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


def validate_input(data):
    if len(data['password']) < 8:
        return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

    if len(data['mobile_number']) != 11:
        return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)

    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({'message': 'DUPLICATE_EMAIL'}, status=401)

    if User.objects.filter(mobile_number=data['mobile_number']).exists():
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
                email=data['email'],
                password=hashed_password,
                mobile_number=data['mobile_number']
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
            user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'access_token': access_token.decode('utf-8')}, status=200)

            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class UserProfileView(APIView):
    @login_decorator
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        serializer_data = serializer.data

        user_info = dict()
        user_info['user_id'] = serializer_data['id']
        user_info['user_name'] = serializer_data['name']
        user_info['email'] = serializer_data['email']
        user_info['mobile_number'] = serializer_data['mobile_number']
        user_info['regist_datetime'] = serializer_data['regist_datetime']

        return Response(user_info)


class UserProfileListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        users_info = list()

        for row in serializer.data:
            dict_data = dict()
            dict_data['user_id'] = row['id']
            dict_data['user_name'] = row['name']
            dict_data['email'] = row['email']
            dict_data['mobile_number'] = row['mobile_number']
            dict_data['regist_datetime'] = row['regist_datetime']

            users_info.append((dict_data))

        return Response(users_info)


class KakaologinView(View):
    def get(self, request):
        kakao_access_code = request.GET.get('code', None)
        print('1', kakao_access_code)
        url = 'https://kauth.kakao.com/oauth/token'
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {
            'grant_type': 'authorization_code',
            'client_id': '4499b173b6f76ea45ebdb3164ece38b7',
            'redirect_url': 'http://localhost:8000/',
            'code': kakao_access_code
        }

        kakao_token_response = requests.post(url, headers=headers, data=body)
        print(kakao_token_response)
        kakao_token = json.loads(kakao_token_response.text).get('kakao_token')
        print(kakao_token)
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            'Authorization': f"""Bearer {kakao_token}""",
            'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers=headers)
        print(kakao_response)
        return HttpResponse(f"""{kakao_response.text}""")

    def post(self, request):
        try:
            kakao_token = request.headers["Authorization"]
            print('kt', kakao_token)
            headers = ({"Authorization": f"Bearer {kakao_token}"})
            url = "https://kapi.kakao.com/v1/user/me"
            response = requests.get(url, headers=headers)
            print('kakao re', response.json)
            kakao_user = response.json()
            print(kakao_user)

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        if User.objects.filter(kakao_id=kakao_user["id"]).exists():
            user_id = User.objects.get(kakao_id=kakao_user["id"]).id
            print('user_id', user_id)
            access_token = jwt.encode({'id': user_id}, SECRET_KEY, algorithm="HS256")
            print('access_token', access_token)
            return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)

        else:
            newUser = User.objects.create(
                kakao_token=kakao_user["id"],
                # email       = kakao_user["properties"]["account_email"], 
                name=kakao_user["properties"]["nickname"]
            )
            access_token = jwt.encode({'id': newUser.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)
