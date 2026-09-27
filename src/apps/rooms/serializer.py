from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomAvalableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'room_number',

            'capacity',

        ]



{
    "room_id": 4,
    "room_name": "Room 204",
    "capacity": 60,
   
  },