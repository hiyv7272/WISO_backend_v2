from django.urls import path
from .views import MoveReserveView, MoveCategoryView

urlpatterns = [
    # path('/reserve', MoveReserve.as_view()),
    # path('/category', MoveCategoryInfo.as_view()),
    path('/reserve', MoveReserveView.as_view({
        'post': 'post',
        'get': 'get',
    })),
    path('/category', MoveCategoryView.as_view({'get': 'list'})),
]