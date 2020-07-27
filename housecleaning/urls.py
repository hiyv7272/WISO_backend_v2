from django.urls import path

from .views import (
    ServiceDayOfWeeksView,
    ServiceStartingTimesView,
    ServiceDurationsView,
    ReserveCycleView,
    HousecleaningReserveInfo,
    OnetimeReserve
)

urlpatterns = [
    path('/reservecycle', ReserveCycleView.as_view()),
    path('/servicedurations', ServiceDurationsView.as_view()),
    path('/servicestartingtimes', ServiceStartingTimesView.as_view()),
    path('/servicedayofweeks', ServiceDayOfWeeksView.as_view()),
    path('/reserve', HousecleaningReserveInfo.as_view()),
    path('/reserve/onetime', OnetimeReserve.as_view()),
]
