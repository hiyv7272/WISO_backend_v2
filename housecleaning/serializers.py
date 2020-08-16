from rest_framework import serializers
from user.utils import sms_service
from datetime import datetime
from .models import (
    HousecleaningReservation,
    ReserveCycle,
    ServiceDuration,
    ServiceStartingTime,
    ServiceDayOfWeek,
)
from user.models import User


class HouseCleanningReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousecleaningReservation
        fields = [
            'USER_id',
            'SERVICE_STARTING_TIME_id',
            'SERVICE_DURATION_id',
            'RESERVE_CYCLE_id',
            'STATUS_id',
            'service_start_date',
            'reserve_location',
            'have_pet',
            'regist_datetime'
        ]

    def create(self, validated_data):
        try:
            HousecleaningReservation(
                USER_id=validated_data['user_id'],
                SERVICE_STARTING_TIME_id=validated_data['service_starting_time_id'],
                SERVICE_DURATION_id=validated_data['service_duration_id'],
                RESERVE_CYCLE_id=validated_data['reserve_cycle_id'],
                STATUS_id=validated_data['status_id'],
                service_start_date=validated_data['service_start_date'],
                reserve_location=validated_data['reserve_location'],
                have_pet=validated_data.get('have_pet', 0) == 1,
                regist_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ).save()

            # user_data = dict()
            # user_data['mobile_number'] = validated_data.mobile_number ## user 객체를 어떻게 가져올까?
            # user_data['address'] = validated_data['reserve_location']
            # sms_service(user_data)

            # sms_service(user_data)

            return HousecleaningReservation
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})