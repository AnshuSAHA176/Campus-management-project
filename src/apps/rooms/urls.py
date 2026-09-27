from rest_framework.routers import DefaultRouter
from .views import RoomView,RoomSearchView,AvalableRoom
from django.urls import path,include


router = DefaultRouter()

router.register(
    '',
    RoomView,
    basename='Room'

)

urlpatterns = [
    path('avalable/',AvalableRoom.as_view(),name='room search'),
    path('search/',RoomSearchView.as_view(),name='room search'),
    path('',include(router.urls))

]