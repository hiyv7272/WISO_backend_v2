from django.urls import path
from .views import MoveReservate, MoveCategoryInfo

urlpatterns = [
    path('/reservate', MoveReservate.as_view()),
    path('/categoryinfo', MoveCategoryInfo.as_view()),
]