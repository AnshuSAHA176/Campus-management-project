from datetime import datetime

from django.db import models
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeOperators,
)
from django.utils import timezone

from psycopg2.extras import DateTimeTZRange


class ClassSession(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="class_sessions",
    )

    teacher = models.ForeignKey(
        "account.Teacher",
        on_delete=models.PROTECT,
        related_name="class_sessions",
    )

    batch = models.ForeignKey(
        "academics.Batch",
        on_delete=models.PROTECT,
        related_name="class_sessions",
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="class_sessions",
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    time_range = DateTimeRangeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    cancellation_reason = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="created_sessions",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [

            # Same teacher + overlapping time
            ExclusionConstraint(
                name="no_teacher_time_overlap",
                expressions=[
                    ("teacher", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
                condition=models.Q(
                    status="SCHEDULED",
                    time_range__isnull=False,
                ),
            ),

            # Same batch + overlapping time
            ExclusionConstraint(
                name="no_batch_time_overlap",
                expressions=[
                    ("batch", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
                condition=models.Q(
                    status="SCHEDULED",
                    time_range__isnull=False,
                ),
            ),

            # Same room + overlapping time
            ExclusionConstraint(
                name="no_room_time_overlap",
                expressions=[
                    ("room", RangeOperators.EQUAL),
                    ("time_range", RangeOperators.OVERLAPS),
                ],
                condition=models.Q(
                    status="SCHEDULED",
                    time_range__isnull=False,
                ),
            ),
        ]

    def save(self, *args, **kwargs):

        start = datetime.combine(
            self.date,
            self.start_time,
        )

        end = datetime.combine(
            self.date,
            self.end_time,
        )

        if timezone.is_naive(start):
            start = timezone.make_aware(start)

        if timezone.is_naive(end):
            end = timezone.make_aware(end)

        self.time_range = DateTimeTZRange(
            start,
            end,
            "[)",
        )

        super().save(*args, **kwargs)


class Activity(models.Model):
    class ActivityType(models.TextChoices):
        CLASS_CREATED = "CLASS_CREATED", "Class Created"
        CLASS_RESCHEDULED = "CLASS_RESCHEDULED", "Class Rescheduled"
        CLASS_CANCELLED = "CLASS_CANCELLED", "Class Cancelled"

    type = models.CharField(
        max_length=50,
        choices=ActivityType.choices
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)