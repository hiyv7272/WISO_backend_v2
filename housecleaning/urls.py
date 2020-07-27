from django.urls import path
from .views import *

urlpatterns = [
    path('/reservecycle', ReserveCycleView.as_view()),
    path('/servicedurations', ServiceDurationsView.as_view()),
    path('/servicestartingtimes', ServiceStartingTimesView.as_view()),
    path('/servicedayofweeks', ServiceDayOfWeeksView.as_view()),
    path('/onetimereservate', OnetimeReservateView.as_view()),
]
