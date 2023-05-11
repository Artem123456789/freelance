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


class ListOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'uuid',
            'title',
            'price',
            ''
        ]
