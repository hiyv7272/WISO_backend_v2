from django.urls import path
from .views import UserProfileView, HousecleaningReservationsView, MoveReservationsView

urlpatterns = [
    path('/userprofile', UserProfileView.as_view()),
    path('/housecleaningreservations', HousecleaningReservationsView.as_view()),
    path('/movereservations', MoveReservationsView.as_view()),
]
