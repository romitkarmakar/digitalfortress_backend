from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from quiz.models import Player


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(writeonly=True)
    name = serializers.CharField(writeonly=True)

    class Meta:
        model = User
        fields = ('email', 'name')

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'], validated_data['name'])
        player = Player.objects.create(
            user=user, name=validated_data['name'], email=validated_data['email'])
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
