from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from app.libs.serialziers import NoneSerializer
from app.orders.handlers.orders_handlers import OrdersHandler
from app.orders.models import (
    Tag,
    Category,
    Order,
    OrderResponse,
    OrderExecutionEmployeeInfo,
    OrderExecutionCustomerInfo,
    LinkToCommunicate,
    CommunicationSource,
)
from app.orders.serializers.orders_serialziers import (
    TagListSerializer,
    CategoryListSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    OrderCreateSerializer,
    OrderResponseCreateSerializer,
    ChooseEmployeeInputSerializer,
    OrderExecutionDetailSerializer,
    OrderExecutionCustomerInfoUpdateSerializer,
    OrderExecutionEmployeeInfoUpdateSerializer,
    LinkToCommunicateListSerializer,
    LinkToCommunicateCreateSerializer,
    CommunicationSourceListSerializer,
    LinkToCommunicateUpdateSerializer,
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
            "employee_orders": OrderListSerializer,
            "execution_detail": OrderExecutionDetailSerializer,
        }[self.action]

    @action(methods=['get'], detail=False)
    def customer_orders(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user)
        serializer = self.get_serializer(orders, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def employee_orders(self, request, *args, **kwargs):
        orders = OrdersHandler().employee_orders(user=self.request.user)
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

    @action(methods=['get'], detail=True)
    def execution_detail(self, request, *args, **kwargs):
        order = self.get_object()

        return Response(self.get_serializer(order).data)

    @action(methods=['post'], detail=True)
    def pay(self, request, *args, **kwargs):
        order = self.get_object()

        order_execution = order.order_execution
        order_execution.is_paid = True
        order_execution.save()

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


class OrderExecutionCustomerInfoViewSet(
    generics.UpdateAPIView,
    GenericViewSet,
):
    queryset = OrderExecutionCustomerInfo.objects.all()

    def get_serializer_class(self):
        return {
            "partial_update": OrderExecutionCustomerInfoUpdateSerializer,
        }[self.action]


class OrderExecutionEmployeeInfoViewSet(
    generics.UpdateAPIView,
    GenericViewSet,
):
    queryset = OrderExecutionEmployeeInfo.objects.all()

    def get_serializer_class(self):
        return {
            "partial_update": OrderExecutionEmployeeInfoUpdateSerializer,
        }[self.action]


class CommunicationSourceViewSet(
    generics.ListAPIView,
    GenericViewSet,
):
    queryset = CommunicationSource.objects.all()

    def get_serializer_class(self):
        return {
            "list": CommunicationSourceListSerializer,
        }[self.action]


class LinkToCommunicateViewSet(
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    GenericViewSet,
):
    def get_queryset(self):
        return LinkToCommunicate.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return {
            "list": LinkToCommunicateListSerializer,
            "create": LinkToCommunicateCreateSerializer,
            "partial_update": LinkToCommunicateUpdateSerializer,
            "delete": NoneSerializer,
        }[self.action]
