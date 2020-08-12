from django.urls import path
from .views import SignUpView, SignInView, KakaologinView, UserViewSet

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/kakaologin', KakaologinView.as_view()),
    path('/list', UserViewSet.as_view({'get': 'list'})),
    path('/profile', UserViewSet.as_view({
        'post': 'create',
        'get': 'retrieve',
        'put': 'update',
    })),
    path('/delete', UserViewSet.as_view({'delete': 'delete'})),
]
