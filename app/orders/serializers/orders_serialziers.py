from rest_framework import serializers

from ..models import (
    Order,
)


class ListOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            ''
        ]