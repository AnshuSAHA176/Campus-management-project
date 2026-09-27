from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticated

from .models import ClassSession
from apps.account.models import Student, User

from .serializer import (
    ClassSeasionTitleSerializer,
    ClassSeasionSerializer,
    TimetableSerializer,
    AgentSerializer,
    RoomSerializer,
    TeacherSecheduleSerializer,
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
from django.db.models import Q


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
                {"detail": "date, start_time and end_time are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        occupied_room_ids = ClassSession.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status=ClassSession.Status.SCHEDULED,
        ).values_list("room_id", flat=True)

        rooms = Room.objects.filter(is_active=True).exclude(id__in=occupied_room_ids)

        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="teacher-schedule",
    )
    def teacher_schedule(self, request):
        
        teacher_id = request.query_params.get("teacher_id")
        date = request.query_params.get("date")

        if not teacher_id:
            if request.user.role == "teacher":
                teacher_id = request.user.teacher_profile.id
            else:
                return Response(
                    {"error": "teacher_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


        if not date:
            return Response(
                {"error": "date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        class_sessions = (
            ClassSession.objects.select_related(
                "teacher",
                "subject",
                "batch",
                "room",
            )
            .filter(
                teacher_id=teacher_id,
                date=date,
                status=ClassSession.Status.SCHEDULED,
            )
            .order_by("start_time")
        )

        serializer = TeacherSecheduleSerializer(
            class_sessions,
            many=True,
        )

        return Response(
            {
                "teacher_id": teacher_id,
                "date": date,
                "classes": serializer.data,
            }
        )


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


{
    "date": "2026-09-28",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "teacher_id": "UUID",
    "batch_id": "UUID",
    "room_id": "UUID",
}


class AgentClassScheduleConflict(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        date = request.query_params.get("date")
        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")

        teacher_id = request.query_params.get("teacher_id")
        batch_id = request.query_params.get("batch_id")
        room_id = request.query_params.get("room_id")

        if not date or not start_time or not end_time:
            return Response(
                {"detail": "date, start_time and end_time are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not teacher_id or not batch_id or not room_id:
            return Response(
                {"detail": ("teacher_id, batch_id and room_id " "are required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conflicts = ClassSession.objects.select_related(
            "subject",
            "teacher",
            "batch",
            "room",
        ).filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status=ClassSession.Status.SCHEDULED,
        )

        conflict_data = []

        teacher_conflict = conflicts.filter(teacher_id=teacher_id).first()

        if teacher_conflict:
            conflict_data.append(
                {
                    "type": "teacher",
                    "class_id": teacher_conflict.id,
                    "subject": teacher_conflict.subject.name,
                    "teacher": teacher_conflict.teacher.full_name,
                    "batch": teacher_conflict.batch.name,
                    "room": teacher_conflict.room.room_number,
                    "start_time": teacher_conflict.start_time,
                    "end_time": teacher_conflict.end_time,
                }
            )

        batch_conflict = conflicts.filter(batch_id=batch_id).first()

        if batch_conflict:
            conflict_data.append(
                {
                    "type": "batch",
                    "class_id": batch_conflict.id,
                    "subject": batch_conflict.subject.name,
                    "teacher": batch_conflict.teacher.full_name,
                    "batch": batch_conflict.batch.name,
                    "room": batch_conflict.room.room_number,
                    "start_time": batch_conflict.start_time,
                    "end_time": batch_conflict.end_time,
                }
            )

        room_conflict = conflicts.filter(room_id=room_id).first()

        if room_conflict:
            conflict_data.append(
                {
                    "type": "room",
                    "class_id": room_conflict.id,
                    "subject": room_conflict.subject.name,
                    "teacher": room_conflict.teacher.full_name,
                    "batch": room_conflict.batch.name,
                    "room": room_conflict.room.room_number,
                    "start_time": room_conflict.start_time,
                    "end_time": room_conflict.end_time,
                }
            )

        if not conflict_data:
            return Response(
                {
                    "has_conflict": False,
                    "conflicts": [],
                }
            )

        return Response(
            {
                "has_conflict": True,
                "conflicts": conflict_data,
            }
        )
