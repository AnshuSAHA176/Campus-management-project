from django.urls import path,include
from .views import (
    RegisterView,
    LoginView,
    StudentProfile,
    TeacherProfile,
    AdminDashBoard,
    AuditLogs,
    TeacherSearchView,
    OurTeacherView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    prefix="all",
    viewset=OurTeacherView,
    basename='teacher_all'
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("student_profile/", StudentProfile.as_view(), name="student"),
    path("teacher_profile/", TeacherProfile.as_view(), name="teacher"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token-to-access"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("dashboard/", AdminDashBoard.as_view(), name="dashboard"),
    path("activitylogs/", AuditLogs.as_view(), name="activitylogs"),
    path("teacher_search/", TeacherSearchView.as_view(), name="teacher_search"),
    path("teacher/", include(router.urls), name="teacher_search"),
]
