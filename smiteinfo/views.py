from rest_framework import generics

from .models import God
from .serializers import GodSerializer, GodDetailSerializer


class GodDetail(generics.RetrieveAPIView):
    """API endpoint to view the details of a specific God."""

    queryset = God.objects.all()
    serializer_class = GodDetailSerializer


class GodList(generics.ListAPIView):
    """API endpoint that allows Gods to be viewed or edited."""

    queryset = God.objects.all().order_by("name")
    serializer_class = GodSerializer
