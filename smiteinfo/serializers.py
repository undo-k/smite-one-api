from .models import God, Item
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "image"]


class GodSerializer(serializers.ModelSerializer):
    top_items = ItemSerializer(many=True)
    win_rate = serializers.DecimalField(
        coerce_to_string=False, max_digits=5, decimal_places=2
    )

    class Meta:
        model = God
        fields = [
            "name",
            "role",
            "win_rate",
            "pick_rate",
            "ban_rate",
            "top_items",
            "frame",
        ]
