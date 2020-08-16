import jwt
import bcrypt

from rest_framework import serializers
from .models import User
from datetime import datetime
from wiso.settings import SECRET_KEY


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def get(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
            if bcrypt.checkpw(validated_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                return access_token
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})

    def user_get_validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError({'message': 'INVALID_PASSWORD'})

        return data

    def create(self, validated_data):
        try:
            hashed_password = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode()
            User(
                name=validated_data['name'],
                email=validated_data['email'],
                password=hashed_password,
                mobile_number=validated_data['mobile_number'],
                regist_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                is_use=True
            ).save()

            return User
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})

    def user_create_validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError({'message': 'INVALID_PASSWORD'})

        if len(data['mobile_number']) != 11:
            raise serializers.ValidationError({'message': 'INVALID_PHONE_NUMBER'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'message': 'DUPLICATE_EMAIL'})

        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_number', 'update_datetime']

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
            instance.update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instance.save()

            return instance
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'update_datetime', 'is_use', 'password']

    def update(self, instance, validated_data):
        try:
            if bcrypt.checkpw(validated_data['password'].encode('utf-8'), instance.password.encode('utf-8')):
                instance.update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                instance.is_use = False
                instance.save()

            return instance
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})
