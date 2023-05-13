from rest_framework import serializers

from ..enitites.orders_entities import ChooseEmployeeInputEntity
from ..models import (
    Order,
    Tag,
    Category,
    OrderResponse,
    LinkToCommunicate,
    CommunicationSource,
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
        ]


class OrderResponseRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderResponse
        fields = [
            'user',
            'text',
            'suggest_price',
            'proposed_deadline',
        ]


class CommunicationSourceRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunicationSource
        fields = [
            'uuid',
            'name',
        ]


class LinkToCommunicateRetrieveSerializer(serializers.ModelSerializer):
    communication_source = CommunicationSourceRetrieveSerializer()

    class Meta:
        model = LinkToCommunicate
        fields = [
            'communication_source',
            'link',
        ]


class OrderRetrieveSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(read_only=True, many=True)
    responses = OrderResponseRetrieveSerializer(read_only=True, many=True)
    links_to_communicate = LinkToCommunicateRetrieveSerializer(read_only=True, many=True)

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


class ChooseEmployeeInputSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data: dict) -> ChooseEmployeeInputEntity:
        employee = User.objects.get(id=validated_data['employee_id'])

        return ChooseEmployeeInputEntity(
            employee=employee,
            customer=validated_data['customer']
        )
