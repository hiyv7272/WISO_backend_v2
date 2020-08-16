from django.urls import path
from .views import KakaologinView, UserViewSet

urlpatterns = [
    path('/kakaologin', KakaologinView.as_view()),
    path('/list', UserViewSet.as_view({'get': 'list'})),
    path('/signup', UserViewSet.as_view({'post': 'sign_up'})),
    path('/signin', UserViewSet.as_view({'post': 'sign_in'})),
    path('/profile', UserViewSet.as_view({
        'post': 'sign_up',
        'get': 'retrieve',
        'put': 'update',
    })),
    path('/delete', UserViewSet.as_view({'delete': 'delete'})),
]
