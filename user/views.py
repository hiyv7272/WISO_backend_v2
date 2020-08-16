import jwt
import json
import bcrypt
import requests

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from wiso.settings import SECRET_KEY
from user.utils import login_decorator

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, UserSignUpSerializer, UserSignInSerializer, UserUpdateSerializer, UserDeleteSerializer


class UserViewSet(viewsets.GenericViewSet):
    def sign_up(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.validate(data):
            serializer.create(data)

        return Response(status=status.HTTP_200_OK)

    def sign_in(self, request):
        data = request.data
        serializer = UserSignInSerializer(data=data)
        if serializer.validate(data):
            return Response({'access_token': serializer.get(data)})

    def list(self, request):
        query_set = User.objects.all().filter(is_use=True)
        serializer = UserSerializer(query_set, many=True)

        return Response(serializer.data)

    @login_decorator
    def retrieve(self, request, pk=None):
        query_set = User.objects.all()
        user = get_object_or_404(query_set, pk=request.user.id)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    @login_decorator
    def update(self, request, pk=None):
        data = request.data
        query_set = User.objects.all()
        user = get_object_or_404(query_set, pk=request.user.id)
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)

    @login_decorator
    def delete(self, request, pk=None):
        user = User.objects.get(id=request.user.id)
        data = request.data
        query_set = User.objects.all()
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(query_set, pk=user.id)
        serializer = UserDeleteSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)


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
