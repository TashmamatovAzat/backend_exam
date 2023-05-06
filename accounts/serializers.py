from rest_framework import serializers
from django.contrib.auth import password_validation as pv

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=40, write_only=True)
    password2 = serializers.CharField(max_length=40, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароль не совпадают')
        return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=40, write_only=True)
    password2 = serializers.CharField(max_length=40, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'is_staff', 'is_superuser', ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароль не совпадают')
        return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        admin = User(
            username=validated_data['username'],
        )
        admin.set_password(validated_data['password'])
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        return admin


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=40, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', ]


    def validate(self, attrs):
        if attrs['username'] and attrs['password'] in User:
            raise serializers.ValidationError('Пароль не совпадают')
        return attrs



