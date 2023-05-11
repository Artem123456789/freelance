from rest_framework import generics
from rest_framework.viewsets import GenericViewSet

from app.orders.models import (
    Tag,
    Category,
    Order,
)
from app.orders.serializers.orders_serialziers import (
    TagListSerializer,
    CategoryListSerializer,
    OrderListSerializer,
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
    GenericViewSet,
):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        return {
            "list": OrderListSerializer,
        }[self.action]
