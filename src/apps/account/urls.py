from django.urls import path
from .views import RegisterView,LoginView,StudentProfile,TeacherProfile


urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('student_profile/',StudentProfile.as_view(),name='student'),
    path('teacher_profile/',StudentProfile.as_view(),name='teacher'),
]

