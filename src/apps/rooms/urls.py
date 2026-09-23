from rest_framework.routers import DefaultRouter
from .views import RoomView
from django.urls import path,include


router = DefaultRouter()

router.register(
    '',
    RoomView,
    basename='Room'

)

urlpatterns = [
    path('',include(router.urls))

]