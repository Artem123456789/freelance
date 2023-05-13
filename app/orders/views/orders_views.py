from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags', 'categories']
    queryset = Order.objects.all()

    def get_serializer_class(self):
        return {
            "list": OrderListSerializer,
            "retrieve": OrderRetrieveSerializer,
            "create": OrderCreateSerializer,
            "choose_employee": ChooseEmployeeInputSerializer,
            "customer_orders": OrderListSerializer,
        }[self.action]

    @action(methods=['get'], detail=False)
    def customer_orders(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user)
        serializer = self.get_serializer(orders, many=True)

        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def choose_employee(self, request, pk, *args, **kwargs):
        order = self.get_object()

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        input_entity = serializer.save()

        OrdersHandler(order=order).choose_employee(input_entity=input_entity)

        return Response()

    @action(methods=['post'], detail=True)
    def complete(self, request, pk, *args, **kwargs):
        order = self.get_object()

        OrdersHandler(order=order).complete_order()

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
