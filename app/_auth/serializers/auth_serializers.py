from rest_framework import serializers
from app.libs.serialziers import BaseSerializer
from app._auth.entities.auth_entities import RegisterInputEntity
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterInputSerializer(BaseSerializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=30, required=True)

    def create(self, validated_data) -> RegisterInputEntity:
        return RegisterInputEntity(**validated_data)


class RegisterResponseSerializer(BaseSerializer):
    user_id = serializers.IntegerField(source="id")


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'customer_description',
            'employee_description',
        ]
