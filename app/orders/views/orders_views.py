from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.orders.handlers.orders_handlers import OrdersHandler
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
    ChooseEmployeeInputSerializer,
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
            "choose_employee": ChooseEmployeeInputSerializer,
        }[self.action]

    @action(methods=['post'], detail=True)
    def choose_employee(self, request, pk, *args, **kwargs):
        order = self.get_object()

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        input_entity = serializer.save()

        OrdersHandler(order=order).choose_employee(input_entity=input_entity)

        return Response()


class OrderResponseViewSet(
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = OrderResponse.objects.all()

    def get_serializer_class(self):
        return {
            "create": OrderResponseCreateSerializer,
        }[self.action]
