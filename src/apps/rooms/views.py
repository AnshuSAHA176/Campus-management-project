from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Room
from .serializer import RoomSerializer

class RoomView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Room.objects.select_related('department')
    serializer_class = RoomSerializer


