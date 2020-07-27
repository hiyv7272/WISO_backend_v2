from django.urls import path
from .views import SignUpView, SignInView, KakaologinView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/kakaologin', KakaologinView.as_view()),
]
