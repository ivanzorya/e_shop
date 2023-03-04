from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class UserResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
