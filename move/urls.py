from django.urls import path
from .views import MoveReserve, MoveCategoryInfo

urlpatterns = [
    path('/reserve', MoveReserve.as_view()),
    path('/category', MoveCategoryInfo.as_view())
]