from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    SemesterViewSet,
    BatchViewSet,
    SubjectViewSet
)

router = DefaultRouter()

router.register(
    "departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    "semesters",
    SemesterViewSet,
    basename="semester",
)

router.register(
    "batches",
    BatchViewSet,
    basename="batch",
)

router.register(
    'subject',
    SubjectViewSet,
    basename='subject'

)

urlpatterns = [
    path("", include(router.urls)),
]