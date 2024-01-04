from django.conf import settings
from django.templatetags.static import static
from rest_framework import serializers

from .models import God, Item


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ["name", "image"]

    def get_image(self, obj):
        return f"{settings.BASE_URL}{static(obj.image.name)}"


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
