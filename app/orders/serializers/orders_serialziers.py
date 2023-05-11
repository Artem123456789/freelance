from rest_framework import serializers

from ..models import (
    Order,
    Tag,
    Category,
    OrderResponse,
    LinkToCommunicate,
    CommunicationSource,
)


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
