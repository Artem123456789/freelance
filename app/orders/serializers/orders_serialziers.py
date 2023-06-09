from rest_framework import serializers

from ..enitites.orders_entities import ChooseEmployeeInputEntity
from ..models import (
    Order,
    Tag,
    Category,
    OrderResponse,
    LinkToCommunicate,
    CommunicationSource,
    OrderExecution,
    OrderExecutionEmployeeInfo,
    OrderExecutionCustomerInfo,
)
from ...libs.serialziers import BaseSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'uuid',
            'name',
        ]


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'uuid',
            'name',
        ]


class OrderListSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(read_only=True, many=True)
    categories = CategoryListSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            'uuid',
            'title',
            'price',
            'tags',
            'categories',
            'is_done',
        ]


class OrderResponseRetrieveSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()

    def get_is_creator(self, order: Order):
        request_user = self.context['request'].user

        return request_user == order.user

    class Meta:
        model = OrderResponse
        fields = [
            'uuid',
            'user',
            'text',
            'suggest_price',
            'proposed_deadline',
            'is_creator',
        ]


class CommunicationSourceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunicationSource
        fields = [
            'uuid',
            'name',
        ]


class LinkToCommunicateListSerializer(serializers.ModelSerializer):
    communication_source = CommunicationSourceListSerializer()

    class Meta:
        model = LinkToCommunicate
        fields = [
            'uuid',
            'communication_source',
            'link',
        ]


class LinkToCommunicateCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LinkToCommunicate
        fields = [
            'user',
            'communication_source',
            'link',
        ]


class LinkToCommunicateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkToCommunicate
        fields = [
            'communication_source',
            'link',
        ]


class OrderRetrieveSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(read_only=True, many=True)
    responses = OrderResponseRetrieveSerializer(read_only=True, many=True)
    links_to_communicate = LinkToCommunicateListSerializer(read_only=True, many=True)
    creator_username = serializers.SerializerMethodField()
    creator_user_id = serializers.SerializerMethodField()

    is_creator = serializers.SerializerMethodField()

    def get_is_creator(self, order: Order):
        request_user = self.context['request'].user

        return request_user == order.user

    def get_creator_username(self, order: Order):
        return order.user.username

    def get_creator_user_id(self, order: Order):
        return order.user.id

    class Meta:
        model = Order
        fields = [
            'uuid',
            'created',
            'title',
            'description',
            'price',
            'tags',
            'responses',
            'links_to_communicate',
            'is_creator',
            'is_employee_selected',
            'is_done',
            'creator_username',
            'creator_user_id',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'uuid',
            'user',
            'title',
            'description',
            'price',
            'tags',
            'categories',
        ]

        read_only_fields = ['uuid']


class OrderResponseCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OrderResponse
        fields = [
            'uuid',
            'user',
            'order',
            'text',
            'suggest_price',
            'proposed_deadline',
        ]

        read_only_fields = ['uuid']


class OrderOrderResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'uuid',
            'title'
        ]


class OrderResponseListSerializer(serializers.ModelSerializer):
    order = OrderOrderResponseSerializer(read_only=True)

    class Meta:
        model = OrderResponse
        fields = [
            'uuid',
            'user',
            'order',
            'text',
            'suggest_price',
            'proposed_deadline',
            'is_seen',
        ]


class OrderResponseUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderResponse
        fields = [
            'is_seen',
        ]


class ChooseEmployeeInputSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    deadline_date = serializers.DateField()

    def create(self, validated_data: dict) -> ChooseEmployeeInputEntity:
        employee = User.objects.get(id=validated_data['employee_id'])

        return ChooseEmployeeInputEntity(
            employee=employee,
            customer=validated_data['customer'],
            deadline_date=validated_data['deadline_date']
        )


class OrderExecutionEmployeeInfoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderExecutionEmployeeInfo
        fields = [
            'uuid',
            'user',
        ]


class OrderExecutionCustomerInfoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderExecutionCustomerInfo
        fields = [
            'uuid',
            'user',
        ]


class OrderExecutionRetrieveSerializer(serializers.ModelSerializer):
    execution_employee_info = OrderExecutionEmployeeInfoRetrieveSerializer(read_only=True)
    execution_customer_info = OrderExecutionCustomerInfoRetrieveSerializer(read_only=True)

    class Meta:
        model = OrderExecution
        fields = [
            'uuid',
            'is_paid',
            'execution_employee_info',
            'execution_customer_info',
        ]


class OrderExecutionDetailSerializer(serializers.ModelSerializer):
    order_execution = OrderExecutionRetrieveSerializer(read_only=True)
    is_creator = serializers.SerializerMethodField()
    is_employee = serializers.SerializerMethodField()

    def get_is_creator(self, order: Order):
        request_user = self.context['request'].user

        return request_user == order.user

    def get_is_employee(self, order: Order):
        request_user = self.context['request'].user

        return order.order_execution.execution_employee_info.user == request_user

    class Meta:
        model = Order
        fields = [
            'uuid',
            'created',
            'title',
            'description',
            'price',
            'is_creator',
            'is_employee',
            'is_done',
            'order_execution',
            'datetime_employee_selected',
            'deadline_date',
            'datetime_compelete',
        ]


class OrderExecutionCustomerInfoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderExecutionCustomerInfo
        fields = [
            'rate',
            'text',
        ]


class OrderExecutionEmployeeInfoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderExecutionEmployeeInfo
        fields = [
            'rate',
            'text',
        ]
