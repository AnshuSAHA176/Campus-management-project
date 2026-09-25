from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import ClassSession, Activity


@receiver(pre_save, sender=ClassSession)
def beforesave(sender, instance, **kwargs):

    # New class
    if not instance.pk:
        instance._old_status = None
        instance._old_date = None
        instance._old_start_time = None
        instance._old_end_time = None
        instance._old_room = None
        return

    try:
        previous_data = ClassSession.objects.get(pk=instance.pk)

        instance._old_status = previous_data.status
        instance._old_date = previous_data.date
        instance._old_start_time = previous_data.start_time
        instance._old_end_time = previous_data.end_time
        instance._old_room = previous_data.room

    except ClassSession.DoesNotExist:
        instance._old_status = None
        instance._old_date = None
        instance._old_start_time = None
        instance._old_end_time = None
        instance._old_room = None


@receiver(post_save, sender=ClassSession)
def Notification(sender, instance, created, **kwargs):

    channel_layer = get_channel_layer()
    messages = []

    # ==========================================
    # CLASS CREATED
    # ==========================================

    if created:

        message = (
            f"New class: {instance.subject.code} "
            f"on {instance.date} "
            f"at {instance.start_time} "
            f"in Room {instance.room.room_number}."
        )

        messages.append(message)

        Activity.objects.create(
            type=Activity.ActivityType.CLASS_CREATED,
            message=message
        )

    # ==========================================
    # CLASS CANCELLED
    # ==========================================

    if (
        not created
        and instance._old_status != ClassSession.Status.CANCELLED
        and instance.status == ClassSession.Status.CANCELLED
    ):

        message = (
            f"{instance.subject.code} class on {instance.date} "
            f"at {instance.start_time} has been cancelled."
        )

        messages.append(message)

        if instance.cancellation_reason:
            messages.append(
                f"Reason: {instance.cancellation_reason}"
            )

        Activity.objects.create(
            type=Activity.ActivityType.CLASS_CANCELLED,
            message=message
        )

    # ==========================================
    # CLASS RESCHEDULED
    # ==========================================

    rescheduled = (
        not created
        and (
            (
                instance._old_date
                and instance._old_date != instance.date
            )
            or (
                instance._old_start_time
                and instance._old_start_time != instance.start_time
            )
            or (
                instance._old_end_time
                and instance._old_end_time != instance.end_time
            )
        )
    )

    if rescheduled:

        message = (
            f"{instance.subject.code} class has been rescheduled."
        )

        messages.append(message)

        Activity.objects.create(
            type=Activity.ActivityType.CLASS_RESCHEDULED,
            message=message
        )

    # ==========================================
    # ROOM CHANGED
    # ==========================================

    if (
        not created
        and instance._old_room
        and instance._old_room != instance.room
    ):

        message = (
            f"{instance.subject.code} on {instance.date} "
            f"has been moved from Room "
            f"{instance._old_room.room_number} to Room "
            f"{instance.room.room_number}."
        )

        messages.append(message)

    # ==========================================
    # SEND WEBSOCKET NOTIFICATION
    # ==========================================

    if messages:

        group_name = f"batch_{instance.batch_id}"

        event = {
            "type": "notification_message",
            "message": "\n".join(messages),
        }

        async_to_sync(
            channel_layer.group_send
        )(
            group_name,
            event
        )