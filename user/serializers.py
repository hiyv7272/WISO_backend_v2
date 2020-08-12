import bcrypt

from rest_framework import serializers
from .models import User
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print('validated_data: ', validated_data)
        hashed_password = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode()
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            password=hashed_password,
            mobile_number=validated_data['mobile_number'],
            regist_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_use=True
        )
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_number', 'update_datetime']

    def update(self, instance, validated_data):
        # validated_data['update_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('update!!')
        print('instance: ', instance)
        print('instance.dir :', dir(instance))
        print('validated_data: ', validated_data)
        instance.name = validated_data.get('name', instance.name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        instance.save()
        return instance


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'update_datetime', 'is_use']

    def update(self, instance, validated_data):
        print('update!!')
        print('instance: ', instance)
        print('instance.dir :', dir(instance))
        print('validated_data: ', validated_data)
        instance.update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        instance.is_use = False
        instance.save()
        print('fin instance: ', instance)
        return instance