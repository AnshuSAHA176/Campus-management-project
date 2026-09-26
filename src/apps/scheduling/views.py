from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,BasePermission,IsAuthenticated

from .models import ClassSession
from apps.account.models import Student,User

from .serializer import ClassSeasionTitleSerializer,ClassSeasionSerializer
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ClassSeasionFilter


class IsAdminOrTeacher(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.role == "teacher"
            )
        )


class IsTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.teacher
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'




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
                return queryset.filter(
                    batch=user.student_profile.batch
                )

            if user.role == "teacher":
                return queryset.filter(
                    teacher=user.teacher_profile #i can changed this in future
                )

            return queryset

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminOrTeacher()]
        
        return [IsAuthenticated()]
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ClassSeasionTitleSerializer( queryset,many=True)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = ClassSeasionSerializer( data = request.data, context={'request': request})
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

            return Response(
                {"detail": message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)

    






{
  "week_start": "2026-09-21",
  "week_end": "2026-09-27",
  "days": [
    {
      "date": "2026-09-21",
      "day": "Monday",
      "classes": [
        {
          "id": "uuid",
          "start_time": "10:00:00",
          "end_time": "11:00:00",
          "subject": {
            "id": 1,
            "name": "Data Structures",
            "code": "BCA-DS"
          },
          "teacher": {
            "id": 1,
            "name": "Dr. Rahul Sharma",
            "profile_picture": "https://..."
          },
          "room": {
            "id": 1,
            "name": "Room 204"
          },
          "status": "SCHEDULED"
        }
      ]
    },
    {
      "date": "2026-09-22",
      "day": "Tuesday",
      "classes": []
    }
  ]
}