from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, Student, Teacher
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    ActivitySerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from django.db.models import Count, Q,Window

from apps.rooms.models import Room
from apps.academics.models import Subject, Batch

from apps.scheduling.models import ClassSession, Activity
from django.utils import timezone
import datetime


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        refresh = RefreshToken.for_user(user=user)
        access = refresh.access_token

        return Response({"access": str(access), "refresh": str(refresh)})


class StudentProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsStudent]
    serializer_class = StudentProfileSerializer
    lookup_url_kwarg = "pk"
    lookup_field = "pk"

    def get_object(self):
        return Student.objects.get(user=self.request.user)


class TeacherProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = TeacherProfileSerializer

    def get_object(self):
        return Teacher.objects.get(user=self.request.user)


class AdminDashBoard(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        overview = User.objects.prefetch_related(
            "student_profile", "teacher_profile"
        ).aggregate(
            total_students=Count("student_profile"),
            total_teachers=Count("teacher_profile"),
        )
        current_time = timezone.now()

        today = timezone.now().date()

        start_of_week = today - datetime.timedelta(days=today.weekday())

        end_of_week = start_of_week + datetime.timedelta(days=6)
        print(end_of_week)
        start_of_next_week = start_of_week + datetime.timedelta(days=7)

        end_of_next_week = start_of_next_week + datetime.timedelta(days=6)

        schedule = (
            ClassSession.objects.select_related("subject", "teacher", "batch", "room")
            .filter(date=current_time.date())
            .aggregate(
                total_classes=Count("id"),
                ongoing_classes=Count(
                    "id",
                    filter=Q(
                        start_time__lte=current_time.time(),
                        end_time__gt=current_time.time(),
                        status=ClassSession.Status.SCHEDULED,
                    ),
                ),
                scheduled_classes=Count(
                    "id",
                    filter=Q(
                        start_time__gt=current_time.time(),
                        status=ClassSession.Status.SCHEDULED,
                    ),
                ),
                completed_classes=Count(
                    "id",
                    filter=Q(status=ClassSession.Status.COMPLETED),
                ),
                classes_this_week=Count(
                    "id", filter=Q(date__range=[start_of_week, end_of_week])
                ),
                classes_next_week=Count(
                    "id", filter=Q(date__range=[start_of_next_week, end_of_next_week])
                ),
                cancelled_this_week=Count(
                    "id",
                    filter=Q(
                        Q(date__range=[start_of_week, end_of_week])
                        & Q(status=ClassSession.Status.CANCELLED)
                    ),
                ),
            )
        )

        rooms = Room.objects.aggregate(
            total_rooms=Count("id", filter=Q(is_active=True)),
            rooms_in_use=Count(
                "id",
                filter=Q(
                    class_sessions__start_time__lte=current_time.time(),
                    class_sessions__end_time__gt=current_time.time(),
                ),
            ),
        )

        batch = Batch.objects.count()

        activity_stats = Activity.objects.aggregate(
    rescheduled_this_week=Count(
        "id",
        filter=Q(
            type=Activity.ActivityType.CLASS_RESCHEDULED,
            created_at__date__range=[
                start_of_week,
                end_of_week,
            ],
        ),
    ),
)

        recent_activity = Activity.objects.order_by("-created_at")[:5]

        return Response(
            {
                "overview": {
                    "total_students": overview["total_students"],
                    "total_teachers": overview["total_teachers"],
                    "total_subjects": Subject.objects.count(),
                    "total_batches": Batch.objects.count(),
                    "total_rooms": Room.objects.count(),
                },
                "today": {
                    "total_classes": schedule["total_classes"],
                    "ongoing_classes": schedule["ongoing_classes"],
                    "scheduled_classes": schedule["scheduled_classes"],
                    "completed_classes": schedule["completed_classes"],
                },
                "schedule": {
                    "classes_this_week": schedule["classes_this_week"],
                    "classes_next_week": schedule["classes_next_week"],
                    "cancelled_this_week": schedule["cancelled_this_week"],
                    "rescheduled_this_week": activity_stats["rescheduled_this_week"],
                },
                "rooms": {
                    "total_rooms": rooms["total_rooms"],
                    "rooms_in_use": rooms["rooms_in_use"],
                    "available_rooms": rooms["total_rooms"] - rooms["rooms_in_use"],
                    "utilization_percentage": round(
                        (rooms["rooms_in_use"] / rooms["total_rooms"]) * 100
                    ),
                },
                "batches": {
                    "active_batches": batch,
                    "total_students": overview["total_students"],
                },
                "recent_activity": [
                    {
                        "type": activity.type,
                        "message": activity.message,
                        "created_at": activity.created_at,
                    }
                    for activity in recent_activity
                ],
            }
        )


class AuditLogs(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Activity.objects.order_by('-created_at')
    serializer_class = ActivitySerializer
    