from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Room
from .serializer import RoomSerializer, RoomAvalableSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import BasePermission


class IsTeacherorAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return (
            request.user.role == "teacher" or request.user.role == "admin"
        ) and request.user.is_authenticated


class RoomView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsTeacherorAdmin()]
        return IsAdminUser

    def get_queryset(self):
        queryset = Room.objects.select_related("department")
        if self.request.user.role == "teacher":
            return queryset.filter(
                department=self.request.user.teacher_profile.department
            )
        return queryset


class RoomSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        rooms = Room.objects.filter(
            Q(room_number__icontains=query) | Q(floor__icontains=query)
        ).values("id", "room_number", "floor",)[:10]

        return Response(list(rooms))


class AvalableRoom(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.query_params.get("date")
        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")

        if not date:
            return Response(
                {"error": "Please provide the date"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not start_time:
            return Response(
                {"error": "Please provide the start time"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not end_time:
            return Response(
                {"error": "Please provide the end time"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        avalable_room = (
            Room.objects.prefetch_related("class_sessions")
            .filter(is_active=True)
            .exclude(
                class_sessions__date=date,
                class_sessions__start_time__lt=end_time,
                class_sessions__end_time__gt=start_time,
            )
        )
        return Response(RoomAvalableSerializer(avalable_room, many=True).data)
