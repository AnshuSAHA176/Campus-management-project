from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticated

from .models import ClassSession
from apps.account.models import Student, User

from .serializer import (
    ClassSeasionTitleSerializer,
    ClassSeasionSerializer,
    TimetableSerializer,
    AgentSerializer,
    RoomSerializer
)
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ClassSeasionFilter
from rest_framework.decorators import action
from rest_framework import generics
from apps.rooms.models import Room
from rest_framework.views import APIView



class IsAdminOrTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.role == "teacher"
        )


class IsTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.teacher

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


class ClassSeasionViewset(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ClassSeasionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassSeasionFilter

    def get_queryset(self):

        user = self.request.user

        queryset = ClassSession.objects.select_related(
            "subject",
            "teacher",
            "batch",
            "room",
        )

        if user.role == "student":
            return queryset.filter(batch=user.student_profile.batch)

        if user.role == "teacher":
            return queryset.filter(
                teacher=user.teacher_profile  # i can changed this in future
            )

        return queryset

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminOrTeacher()]

        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ClassSeasionTitleSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def timetable(self, request):
        query = self.filter_queryset(self.get_queryset()).order_by("date", "start_time")

        serializer = TimetableSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ClassSeasionSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()

        except IntegrityError as exc:

            error = str(exc)

            if "no_teacher_time_overlap" in error:
                message = "The teacher already has a class during this time."

            elif "no_batch_time_overlap" in error:
                message = "The batch already has a class during this time."

            elif "no_room_time_overlap" in error:
                message = "The room is already booked during this time."

            else:
                message = "The class could not be scheduled because of a conflict."

            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    @action(
        detail=False,
        methods=["GET"],
        url_path="available-rooms",
    )
    def available_rooms(self, request):
            date = request.query_params.get("date")
            start_time = request.query_params.get("start_time")
            end_time = request.query_params.get("end_time")
    
            if not date or not start_time or not end_time:
                return Response(
                    {
                        "detail": "date, start_time and end_time are required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
    
            occupied_room_ids = ClassSession.objects.filter(
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status=ClassSession.Status.SCHEDULED,
            ).values_list("room_id", flat=True)
    
            rooms = Room.objects.filter(
                is_active=True
            ).exclude(
                id__in=occupied_room_ids
            )
    
            serializer = RoomSerializer(rooms, many=True)
    
            return Response(serializer.data)

class AgentToolsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassSeasionFilter

    serializer_class = AgentSerializer

    def get_queryset(self):

        user = self.request.user

        queryset = ClassSession.objects.select_related(
            "subject",
            "teacher",
            "batch",
            "room",
        )

        if user.role == "student":
            return queryset.filter(batch=user.student_profile.batch)

        if user.role == "teacher":
            return queryset.filter(
                teacher=user.teacher_profile  # i can changed this in future
            )
        
        return queryset

{"date": "2026-09-28",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "teacher_id": "UUID",
  "batch_id": "UUID",
  "room_id": "UUID"}
class AgentClassSedulesConflits(APIView):
    ...