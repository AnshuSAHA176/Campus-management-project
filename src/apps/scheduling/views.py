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

    def get_object(self):
        user = self.request.user
        if user.role == 'student':

            profile = get_object_or_404(Student,user=user)

            return ClassSession.objects.filter(batch = profile.batch)

        elif user.role == 'teacher':
            if self.request.method in ['list','retrieve']:
               
                return ClassSession.objects.select_related('subject','teacher','batch','room')
                
            
            return ClassSession.objects.select_related('subject','teacher','batch','room').filter(teacher=user)

        return ClassSession.objects.select_related('subject','teacher','batch','room')

    def get_permissions(self):
        if self.request.method in ['create','update','partial_update','destroy']:
            return [IsAdminOrTeacher()]
        
        return [IsAuthenticated()]
    

    def list(self, request, *args, **kwargs):

        serializer = ClassSeasionTitleSerializer(many=True)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = ClassSeasionSerializer( data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    






