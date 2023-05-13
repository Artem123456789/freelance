from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet

from app._auth.serializers.auth_serializers import (
    RegisterInputSerializer,
    RegisterResponseSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from app._auth.handlers.auth_handlers import AuthHandler
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def register(request):
    serializer = RegisterInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    input_entity = serializer.save()
    response = AuthHandler().register(input_entity)

    return Response(RegisterResponseSerializer(response).data, status=status.HTTP_201_CREATED)


class UserViewSet(
    generics.RetrieveAPIView,
    GenericViewSet,
):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return {
            "retrieve": UserProfileSerializer,
            "profile": UserProfileSerializer,
            "update_profile": UserProfileUpdateSerializer,
        }[self.action]

    @action(methods=['get'], detail=False)
    def profile(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def update_profile(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.customer_description = serializer.validated_data['customer_description']
        user.employee_description = serializer.validated_data['employee_description']
        user.save()

        return Response(serializer.data)
