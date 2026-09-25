from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from .models import User,Student,Teacher
from .serializer import RegisterSerializer,LoginSerializer,StudentProfileSerializer,TeacherProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from django.db.models import Count

from apps.rooms.models import Room
from apps.academics.models import Subject,Batch

from apps.scheduling.models import ClassSession

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'
    
class IsTeacher(BasePermission):

    def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role == 'teacher'


class RegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user=user)
        access = refresh.access_token

        return Response(
            {
                'access':str(access),
                'refresh':str(refresh)
            }
        )

class  StudentProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsStudent]
    serializer_class = StudentProfileSerializer
    lookup_url_kwarg='pk'
    lookup_field='pk'
    
    def get_object(self):
        return Student.objects.get(user=self.request.user)


class  TeacherProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = TeacherProfileSerializer
    def get_object(self):
        return Teacher.objects.get(user=self.request.user)




class AdminDashBoard(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request):

        overview = User.objects.prefetch_related(
            'student_profile',
            'teacher_profile'
            ).aggregate(

                total_students = Count('student_profile'),
                total_teachers = Count('teacher_profile')
                
                
                )

        today = ClassSession.objects.select_related('subject',"teacher",'batch','room')
        










        return Response(
            {
    "overview": {
        "total_students": overview['total_students'] ,
        "total_teachers": overview['total_teachers'],
        "total_subjects": Subject.objects.count(),
        "total_batches": Batch.objects.count(),
        "total_rooms": Room.objects.count()
    },

    "today": {
        "total_classes": 14,
        "scheduled_classes": 11,
        "ongoing_classes": 2,
        "completed_classes": 1,
        "cancelled_classes": 0
    },

    "schedule": {
        "classes_this_week": 68,
        "classes_next_week": 72,
        "cancelled_this_week": 4,
        "rescheduled_this_week": 6
    },

    "rooms": {
        "total_rooms": 12,
        "rooms_in_use": 8,
        "available_rooms": 4,
        "utilization_percentage": 66.67
    },

    "people": {
        "active_students": 116,
        "inactive_students": 4,
        "active_teachers": 17,
        "inactive_teachers": 1
    },

    "batches": {
        "active_batches": 8,
        "total_students": 120
    },

    "recent_activity": [
        {
            "type": "CLASS_CREATED",
            "message": "BCA-DS-301 class created for Batch 2.",
            "created_at": "2026-09-25T10:30:00Z"
        },
        {
            "type": "CLASS_RESCHEDULED",
            "message": "DBMS class moved from Room 205 to Room 204.",
            "created_at": "2026-09-25T10:15:00Z"
        },
        {
            "type": "CLASS_CANCELLED",
            "message": "BCA-DS-301 class cancelled.",
            "created_at": "2026-09-25T09:45:00Z"
        }
    ]
}
        )