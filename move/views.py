import json

from user.utils import login_decorator

from rest_framework import viewsets, status
from rest_framework.response import Response

from move.models import MoveReservation, MoveCategory
from .serializers import MoveReserveSerializer, MoveCategorySerializer


class MoveReserveView(viewsets.GenericViewSet):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        data['user_id'] = request.user.id
        query_set = MoveReservation.objects.all()
        serializer = MoveReserveSerializer(query_set, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(validated_data=data)

        return Response(status=status.HTTP_200_OK)

    @login_decorator
    def get(self, request):
        query_set = MoveReservation.objects.select_related(
            'USER',
            'MOVE_CATEGORY').filter(USER_id=request.user.id).order_by('id')
        serializer = MoveReserveSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MoveCategoryView(viewsets.GenericViewSet):
    def list(self, request):
        query_set = MoveCategory.objects.all()
        serializer = MoveCategorySerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
