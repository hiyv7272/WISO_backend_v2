from rest_framework import serializers
from .models import MoveReservation, MoveCategory
from user.utils import sms_service
from datetime import datetime


class MoveReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveReservation
        fields = ['USER_id', 'MOVE_CATEGORY_id', 'address', 'mobile_number']

    def create(self, validated_data):
        try:
            MoveReservation(
                USER_id=validated_data['user_id'],
                MOVE_CATEGORY_id=validated_data['move_category_id'],
                address=validated_data['address'],
                mobile_number=validated_data['mobile_number'],
                regist_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ).save()

            user_data = dict()
            user_data['mobile_number'] = validated_data['mobile_number']
            user_data['address'] = validated_data['address']
            sms_service(user_data)

            return MoveReservation
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})


class MoveCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveCategory
        fields = ['id', 'name']
