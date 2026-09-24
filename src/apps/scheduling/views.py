from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,BasePermission,IsAuthenticated

from .models import ClassSession
from apps.account.models import Student,User
from django.shortcuts import get_object_or_404
from .serializer import ClassSeasionTitleSerializer,ClassSeasionSerializer
from rest_framework.response import Response


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
        queryset = self.get_queryset()
        serializer = ClassSeasionTitleSerializer( queryset,many=True)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = ClassSeasionSerializer( data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    






