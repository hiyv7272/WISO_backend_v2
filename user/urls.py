from django.urls import path
from .views import SignUpView, SignInView, KakaologinView, UserProfileView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/kakaologin', KakaologinView.as_view()),
    path('/list', UserProfileView.as_view({'get': 'list'})),
    path('/profile', UserProfileView.as_view({
        'post': 'create',
        'get': 'retrieve',
        'put': 'update',
    })),
    path('/delete', UserProfileView.as_view({'delete': 'delete'})),
]
