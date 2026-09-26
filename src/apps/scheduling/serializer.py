from rest_framework import serializers
from .models import ClassSession

from django.utils import timezone
from apps.academics.models import Subject

from django.db import transaction
from apps.account.models import Teacher
from django.db.models import Q
from apps.academics.models import Batch

from apps.rooms.models import Room
from .notification_clint import wanotification, beforeclass
import datetime


class ClassSeasionTitleSerializer(serializers.ModelSerializer):
    teacher_picture = serializers.ImageField(source="teacher.profile_picture")

    class Meta:
        model = ClassSession
        fields = ["id", "teacher", "room", "start_time", "teacher_picture"]


class ClassSeasionSerializer(serializers.ModelSerializer):

    teacher_picture = serializers.ImageField(
        source="teacher.profile_picture", read_only=True
    )

    class Meta:
        model = ClassSession
        fields = "__all__"

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()

        request = self.context.get("request")

        if request and request.user.is_authenticated and request.user.role == "teacher":
            extra_kwargs["teacher"] = {"read_only": True}

        extra_kwargs["created_by"] = {"read_only": True}

        return extra_kwargs

    def validate(self, attrs):
        request = self.context.get("request")

        if request.user.role == "teacher":
            teacher = request.user.teacher_profile
        else:
            teacher = attrs.get(
                "teacher", self.instance.teacher if self.instance else None
            )

        # Existing values + PATCH values
        date = attrs.get("date", self.instance.date if self.instance else None)

        start_time = attrs.get(
            "start_time", self.instance.start_time if self.instance else None
        )

        end_time = attrs.get(
            "end_time", self.instance.end_time if self.instance else None
        )

        subject = attrs.get("subject", self.instance.subject if self.instance else None)

        batch = attrs.get("batch", self.instance.batch if self.instance else None)

        room = attrs.get("room", self.instance.room if self.instance else None)

        status_value = attrs.get(
            "status", self.instance.status if self.instance else None
        )

        cancellation_reason = attrs.get(
            "cancellation_reason",
            self.instance.cancellation_reason if self.instance else "",
        )

        # -------------------------
        # Cancellation validation
        # -------------------------

        if (
            status_value == ClassSession.Status.CANCELLED
            and not cancellation_reason.strip()
        ):
            raise serializers.ValidationError(
                {
                    "cancellation_reason": "A cancellation reason is required when cancelling a class."
                }
            )

        # -------------------------
        # Basic validation
        # -------------------------

        if not request.user.is_staff:
            if date < timezone.now().date():
                raise serializers.ValidationError("Class date cannot be in the past.")

            if date == timezone.now().date() and start_time < timezone.now().time():
                raise serializers.ValidationError("Start time cannot be in the past.")

        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before the end time.")

        # -------------------------
        # Active object validation
        # -------------------------

        if not subject.is_active:
            raise serializers.ValidationError("Subject is not active.")

        if not batch.is_active:
            raise serializers.ValidationError("Batch is not active.")

        if not room.is_active:
            raise serializers.ValidationError("Room is not active.")

        # -------------------------
        # Department validation
        # -------------------------

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

        # -------------------------
        # Conflict validation
        # -------------------------

        time_overlap = ClassSession.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status=ClassSession.Status.SCHEDULED,
        )

        if self.instance:
            time_overlap = time_overlap.exclude(pk=self.instance.pk)

        conflicts = time_overlap.filter(
            Q(teacher=teacher) | Q(batch=batch) | Q(room=room)
        ).select_related("teacher", "batch", "room")

        for conflict in conflicts:
            if conflict.teacher_id == teacher.id:
                raise serializers.ValidationError(
                    "The teacher already has a class during this time."
                )

            if conflict.batch_id == batch.id:
                raise serializers.ValidationError(
                    "The batch already has a class during this time."
                )

            if conflict.room_id == room.id:
                raise serializers.ValidationError(
                    f"The room is already booked from "
                    f"{conflict.start_time} to {conflict.end_time}."
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        request = self.context.get("request")

        # Teacher creates class for themselves
        if request.user.role == "teacher":

            validated_data["teacher"] = request.user.teacher_profile

        teacher = Teacher.objects.select_for_update().filter(
            pk=validated_data["teacher"].pk
        )

        batch = Batch.objects.select_for_update().get(pk=validated_data["batch"].pk)

        room = Room.objects.select_for_update().get(pk=validated_data["room"].pk)

        # Always set creator from authenticated user
        validated_data["created_by"] = request.user

        instance = ClassSession.objects.create(**validated_data)
        transaction.on_commit(lambda: wanotification.delay())

        notification_time = timezone.make_aware(
            datetime.datetime.combine(date=instance.date, time=instance.start_time)
        ) - datetime.timedelta(minutes=15)

        transaction.on_commit(
            lambda: beforeclass.apply_async(args=[instance.id], eta=notification_time)
        )

        return instance


class TimetableSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(source="subject.name", read_only=True)

    teacher_name = serializers.CharField(source="teacher.full_name", read_only=True)

    batch_name = serializers.CharField(source="batch.name", read_only=True)

    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = ClassSession
        fields = [
            "id",
            "date",
            "start_time",
            "end_time",
            "subject_name",
            "teacher_name",
            "batch_name",
            "room_name",
            "status",
        ]


class AgentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.full_name")
    subject_name = serializers.CharField(source="subject.name")
    room_name = serializers.CharField(source="room.room_number")
    batch_name = serializers.CharField(source="batch.name")
    class Meta:
        model = ClassSession
        fields = [
            "id",
            "date",
            "start_time",
            "end_time",
            "teacher_name",
            "subject_name",
            "room_name",
            "status",
            'batch_name'
        ]


