from django.db.models import Sum
from rest_framework import serializers
from app.libs.serialziers import BaseSerializer
from app._auth.entities.auth_entities import RegisterInputEntity

from django.contrib.auth import get_user_model

from app.orders.handlers.orders_handlers import OrdersHandler
from app.orders.models import (
    OrderExecutionEmployeeInfo,
    OrderExecutionCustomerInfo,
    LinkToCommunicate,
    Order,
)
from app.orders.serializers.orders_serialziers import (
    LinkToCommunicateListSerializer,
    OrderListSerializer,
)

User = get_user_model()


class RegisterInputSerializer(BaseSerializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=30, required=True)
    customer_description = serializers.CharField()
    employee_description = serializers.CharField()

    def create(self, validated_data) -> RegisterInputEntity:
        return RegisterInputEntity(**validated_data)


class RegisterResponseSerializer(BaseSerializer):
    user_id = serializers.IntegerField(source="id")


class UserProfileSerializer(serializers.ModelSerializer):
    rate_as_employee = serializers.SerializerMethodField()
    rate_as_customer = serializers.SerializerMethodField()
    links_to_communicate = serializers.SerializerMethodField()
    customer_orders = serializers.SerializerMethodField()
    employee_orders = serializers.SerializerMethodField()

    def get_rate_as_employee(self, user: User):
        rate = OrderExecutionEmployeeInfo.objects.filter(user=user).aggregate(Sum('rate'))

        return rate['rate__sum']

    def get_rate_as_customer(self, user: User):
        rate = OrderExecutionCustomerInfo.objects.filter(user=user).aggregate(Sum('rate'))

        return rate['rate__sum']

    def get_links_to_communicate(self, user: User):
        return LinkToCommunicateListSerializer(LinkToCommunicate.objects.filter(user=user), many=True).data

    def get_customer_orders(self, user: User):
        return OrderListSerializer(Order.objects.filter(user=user), many=True).data

    def get_employee_orders(self, user: User):
        return OrderListSerializer(OrdersHandler().employee_orders(user=user), many=True).data

    class Meta:
        model = User
        fields = [
            'customer_description',
            'employee_description',
            'rate_as_employee',
            'rate_as_customer',
            'links_to_communicate',
            'customer_orders',
            'employee_orders',
        ]
