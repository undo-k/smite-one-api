from .models import God, Item, Match, MatchPlayer
from rest_framework import generics
from .serializers import GodSerializer

class GodDetail(generics.RetrieveAPIView):
    """API endpoint to view the details of a specific God."""

    queryset = God.objects.all()
    serializer_class = GodSerializer


class GodList(generics.ListAPIView):
    """API endpoint that allows Gods to be viewed or edited."""

    queryset = God.objects.all().order_by("name")
    serializer_class = GodSerializer
