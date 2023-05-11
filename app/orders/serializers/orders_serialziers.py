from rest_framework import serializers

from ..models import (
    Order,
    Tag,
    Category,
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
