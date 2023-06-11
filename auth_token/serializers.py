from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from auth_token import models


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile_phone_number', 'birth_date', 'gender']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile_phone_number = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile_phone_number', 'birth_date', 'gender']


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    mobile_phone_number = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    birth_date = serializers.DateTimeField(required=False, allow_null=True)
    gender = serializers.ChoiceField(models.GENDER_CHOICES, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.User
        fields = ('email', 'password',
                  'mobile_phone_number',
                  'first_name', 'last_name',
                  'gender', 'birth_date'
                  )