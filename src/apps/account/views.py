from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import User,Student
from .serializer import RegisterSerializer,LoginSerializer,StudentProfileSerializer,TeacherProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


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
    def get_queryset(self):
        return Student.objects.get(user=self.request.user)


class  TeacherProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = TeacherProfileSerializer
    def get_queryset(self):
        return Student.objects.get(user=self.request.user)
