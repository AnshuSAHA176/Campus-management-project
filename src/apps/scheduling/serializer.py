from rest_framework import serializers
from .models import ClassSession

from django.utils import timezone
from apps.academics.models import Subject

from django.db import transaction
from apps.account.models import Teacher

from apps.academics.models import Batch

from apps.rooms.models import Room

class ClassSeasionTitleSerializer(serializers.ModelSerializer):
    teacher_picture = serializers.ImageField(source = 'teacher.profile_picture')
    class Meta:
        model = ClassSession
        fields = [
            'id',
            'teacher',
            'room',
            'start_time',
            'teacher_picture'
        ]



class ClassSeasionSerializer(serializers.ModelSerializer):

    teacher_picture = serializers.ImageField(
        source="teacher.profile_picture",
        read_only=True
    )

    class Meta:
        model = ClassSession
        fields = "__all__"

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()

        request = self.context.get("request")

        if request and request.user.role == "teacher":
            extra_kwargs["teacher"] = {
                "read_only": True
            }

        extra_kwargs["created_by"] = {
            "read_only": True
        }

        return extra_kwargs

    def validate(self, attrs):

        request = self.context.get("request")


        if request.user.role == "teacher":
            teacher = request.user.teacher_profile
        else:
            teacher = attrs["teacher"]

      

        if not request.user.is_staff:

            if attrs["date"] < timezone.now().date():
                raise serializers.ValidationError(
                    "Class date cannot be in the past."
                )

            if (
                attrs["date"] == timezone.now().date()
                and attrs["start_time"] < timezone.now().time()
            ):
                raise serializers.ValidationError(
                    "Start time cannot be in the past."
                )

        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(
                "Start time must be before the end time."
            )


        subject = attrs["subject"]
        batch = attrs["batch"]
        room = attrs["room"]

        print("Teacher:", teacher)
        print("Teacher department:", teacher.department_id)
        print("Subject:", subject)
        print("Subject department:", subject.department_id)

                

        if not subject.is_active:
            raise serializers.ValidationError(
                "Subject is not active."
            )

        if not batch.is_active:
            raise serializers.ValidationError(
                "Batch is not active."
            )

        if not room.is_active:
            raise serializers.ValidationError(
                "Room is not active."
            )

    

        department = teacher.department

        if subject.department != department:
            raise serializers.ValidationError(
                "The subject does not belong to the teacher's department."
            )

        if batch.department != department:
            raise serializers.ValidationError(
                "The batch does not belong to the teacher's department."
            )

        if room.department != department:
            raise serializers.ValidationError(
                "The room does not belong to the teacher's department."
            )

        

        time_overlap = ClassSession.objects.filter(
            date=attrs["date"],
            start_time__lt=attrs["end_time"],
            end_time__gt=attrs["start_time"],
        )

        # Don't compare the object with itself during update
        if self.instance:
            time_overlap = time_overlap.exclude(
                pk=self.instance.pk
            )

      
        if time_overlap.filter(
            teacher=teacher
        ).exists():

            raise serializers.ValidationError(
                "The teacher already has a class during this time."
            )

     
        if time_overlap.filter(
            batch=batch
        ).exists():

            raise serializers.ValidationError(
                "The batch already has a class during this time."
            )

       
        room_conflict = time_overlap.filter(
            room=room
        ).first()

        if room_conflict:

            raise serializers.ValidationError(
                f"The room is already booked from "
                f"{room_conflict.start_time} "
                f"to {room_conflict.end_time}."
            )

        return attrs
    @transaction.atomic
    def create(self, validated_data):

        request = self.context.get("request")

        
        # Teacher creates class for themselves
        if request.user.role == "teacher":

            validated_data["teacher"] = (
                request.user.teacher_profile
            )

        teacher = (
            Teacher.objects.select_for_update().filter(
                pk=validated_data['teacher'].pk
            )
        )

        batch = (
            Batch.objects.select_for_update().get(
                pk=validated_data['batch'].pk
            )
        )

        room = (
            Room.objects.select_for_update().get(
                pk=validated_data['room'].pk
            )
        )

        
        # Always set creator from authenticated user
        validated_data["created_by"] = request.user

        return ClassSession.objects.create(
            **validated_data
        )


{
  "department": 1,
  "semester": 3,
  "subject": 5,
  "batch": 2,
  "room": 204,
  "date": "2026-09-28",
  "start_time": "10:00",
  "end_time": "11:00"
}