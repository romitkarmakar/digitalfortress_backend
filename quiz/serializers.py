from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from quiz.models import Player, Round, Clue


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'name')

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'], validated_data['name'])
        player = Player.objects.create(
            user=user, name=validated_data['name'], email=validated_data['email'], image=validated_data['image'])
        return User


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('user', 'name', 'email', 'image', 'score')


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        return serializers.ValidationError("Unable to log in. Try again!")


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ('question', 'round_number')
