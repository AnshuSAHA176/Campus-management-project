from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    SemesterViewSet,
    BatchViewSet,
    SubjectViewSet,
    BatchSearchView,
    SubjectSearch,
    DeparmentSearch,
    BatchAllTItleView
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
    "subject",
    SubjectViewSet,
    basename="subject",
)

urlpatterns = [
    
    path(
        "departments/all/",
        DeparmentSearch.as_view(),
        name="batch-search",
    ),
    path(
        "batches/all/",
        BatchAllTItleView.as_view(),
        name="batch-search",
    ),
    path(
        "batches/search/",
        BatchSearchView.as_view(),
        name="batch-search",
    ),
    path(
        "subject/search/",
        SubjectSearch.as_view(),
        name="batch-search",
    ),
    path(
        "",
        include(router.urls),
    ),
]