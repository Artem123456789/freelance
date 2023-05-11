from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet

from app.orders.models import (
    Tag,
    Category,
    Order,
    OrderResponse,
)
from app.orders.serializers.orders_serialziers import (
    TagListSerializer,
    CategoryListSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    OrderCreateSerializer,
    OrderResponseCreateSerializer,
)


class TagViewSet(
    generics.ListAPIView,
    GenericViewSet,
):
    queryset = Tag.objects.all()

    def get_serializer_class(self):
        return {
            "list": TagListSerializer,
        }[self.action]


class CategoryViewSet(
    generics.ListAPIView,
    GenericViewSet,
):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return {
            "list": CategoryListSerializer,
        }[self.action]


class OrderViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags', 'categories']

    def get_serializer_class(self):
        return {
            "list": OrderListSerializer,
            "retrieve": OrderRetrieveSerializer,
            "create": OrderCreateSerializer,
        }[self.action]


class OrderResponseViewSet(
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = OrderResponse.objects.all()

    def get_serializer_class(self):
        return {
            "create": OrderResponseCreateSerializer,
        }[self.action]
