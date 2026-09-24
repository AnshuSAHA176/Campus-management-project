from django.db import models
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeOperators,
)
from django.db.models import F
from django.utils import timezone
from datetime import datetime


class ClassSession(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="class_sessions"
    )

    teacher = models.ForeignKey(
        "account.Teacher",
        on_delete=models.PROTECT,
        related_name="class_sessions"
    )

    batch = models.ForeignKey(
        "academics.Batch",
        on_delete=models.PROTECT,
        related_name="class_sessions"
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="class_sessions"
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Used by PostgreSQL to detect overlapping sessions
    time_range = DateTimeRangeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )

    cancellation_reason = models.TextField(blank=True)

    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="created_sessions"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [

            # Same teacher cannot have overlapping classes
            ExclusionConstraint(
                name="no_teacher_time_overlap",
                expressions=[
                    ("teacher", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
            ),

            # Same batch cannot have overlapping classes
            ExclusionConstraint(
                name="no_batch_time_overlap",
                expressions=[
                    ("batch", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
            ),

            # Same room cannot have overlapping classes
            ExclusionConstraint(
                name="no_room_time_overlap",
                expressions=[
                    ("room", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
            ),
        ]

    def save(self, *args, **kwargs):

        start = datetime.combine(
            self.date,
            self.start_time
        )

        end = datetime.combine(
            self.date,
            self.end_time
        )

        if timezone.is_naive(start):
            start = timezone.make_aware(start)

        if timezone.is_naive(end):
            end = timezone.make_aware(end)

        # [) means:
        # start included
        # end excluded
        #
        # 10:00-11:00
        # 11:00-12:00
        #
        # are therefore allowed.
        from psycopg2.extras import DateTimeTZRange

        self.time_range = DateTimeTZRange(
            start,
            end,
            "[)"
        )

        super().save(*args, **kwargs)

class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CANCELLED = "CANCELLED", "Cancelled"

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="bookings"
    )

    requested_by = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="room_bookings"
    )

    class_session = models.OneToOneField(
        ClassSession,
        on_delete=models.CASCADE,
        related_name="booking"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    reason = models.TextField(
        blank=True
    )

    approved_by = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_bookings"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Timetable(models.Model):

    name = models.CharField(
        max_length=150
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        related_name="timetables"
    )

    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.PROTECT,
        related_name="timetables"
    )

    batch = models.ForeignKey(
        "academics.Batch",
        on_delete=models.PROTECT,
        related_name="timetables"
    )

    academic_year = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

