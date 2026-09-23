from django.urls import path
from .views import RegisterView,LoginView,StudentProfile,TeacherProfile
from rest_framework_simplejwt.views import TokenRefreshView,TokenBlacklistView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('student_profile/',StudentProfile.as_view(),name='student'),
    path('teacher_profile/',StudentProfile.as_view(),name='teacher'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh-token-to-access'),
    path('logout/',TokenBlacklistView.as_view(),name='logout'),
]

