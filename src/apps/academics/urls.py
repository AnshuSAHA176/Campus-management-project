from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet
from django.urls import include,path

router = DefaultRouter()

router.register(
    "",
    DepartmentViewSet,
    basename="Department",
)
urlpatterns = [
    path("", include(router.urls)),
]
