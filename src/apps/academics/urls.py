from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet,SemesterViewSet,BatchViewSet
from django.urls import include,path

router = DefaultRouter()

router.register(
    "",
    DepartmentViewSet,
    basename="department",
)
router.register(
    "",
    SemesterViewSet,
    basename="semester",
)
router.register(
    "",
    BatchViewSet,
    basename="batch",
)


urlpatterns = [
    path("", include(router.urls)),
]

