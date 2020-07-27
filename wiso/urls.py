from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('housecleaning',include('housecleaning.urls')),
    path('move',include('move.urls')),
]
