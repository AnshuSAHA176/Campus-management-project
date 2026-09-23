from django.db import models

class Room(models.Model):

    class RoomType(models.TextChoices):
        CLASSROOM = "CLASSROOM", "Classroom"
        COMPUTER_LAB = "COMPUTER_LAB", "Computer Lab"
        LAB = "LAB", "Laboratory"
        SEMINAR_HALL = "SEMINAR_HALL", "Seminar Hall"

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=30)

    building = models.CharField(max_length=100)

    floor = models.PositiveSmallIntegerField()

    capacity = models.PositiveIntegerField()

    room_type = models.CharField(
        max_length=30,
        choices=RoomType.choices
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["building", "room_number"],
                name="unique_room"
            )
        ]