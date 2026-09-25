from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from apps.account.models import User

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        self.batch_group = None

        if user.role == User.RoleChoices.STUDENT:

            batch_id = await self.get_student_batch_id(user.id)

            if batch_id is not None:
                self.batch_group = f"batch_{batch_id}"

                await self.channel_layer.group_add(
                    self.batch_group,
                    self.channel_name
                )

        await self.accept()

    async def disconnect(self, close_code):

        if self.batch_group:
            await self.channel_layer.group_discard(
                self.batch_group,
                self.channel_name
            )

    async def notification_message(self, event):

        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"],
        }))

    @database_sync_to_async
    def get_student_batch_id(self, user_id):

        user = User.objects.select_related(
            "student_profile__batch"
        ).get(id=user_id)

        return user.student_profile.batch_id