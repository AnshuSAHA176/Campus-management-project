from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ClassSeasionViewset, AgentToolsView


router = DefaultRouter()

router.register(
    '',
    ClassSeasionViewset,
    basename='class-session'
)

urlpatterns = [
    path('tools/', AgentToolsView.as_view(), name='schedule-tools'),
    path('', include(router.urls)),
]