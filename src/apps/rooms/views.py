from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import Room
from .serializer import RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

class RoomView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Room.objects.select_related('department')
    serializer_class = RoomSerializer


class RoomSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        rooms = Room.objects.filter(
            Q(room_number__icontains=query) |
            Q(floor__icontains=query)
        ).values(
            "id",
            "room_number",
            "floor",
        )[:10]

        return Response(list(rooms))