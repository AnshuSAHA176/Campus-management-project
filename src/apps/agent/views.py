from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from .agent import get_agent

from rest_framework.response import Response

from langchain.messages import SystemMessage, HumanMessage

from django.http import StreamingHttpResponse
import json


system_message = """
TEACHER SCHEDULE RULES:
- When a teacher asks for "my schedule", "my timetable", or similar:
  call teacher_schedule without teacher_id. The API will automatically
  identify the authenticated teacher.

- When an admin or other non-teacher asks for a teacher's schedule:
  the teacher's name is required.
  If the teacher's name is not provided, DO NOT call teacher_schedule.
  Ask the user to provide the teacher's name.

- If the user provides a teacher name:
  1. Use search_teachers to find the teacher.
  2. If exactly one teacher is found, use that teacher's ID.
  3. If multiple teachers are found, ask the user to clarify.
  4. Then call teacher_schedule with the resolved teacher_id.

Examples:
- Teacher: "Show my schedule tomorrow."
  → call teacher_schedule with teacher_id=None.

- Admin: "Show my schedule tomorrow."
  → ask: "Which teacher's schedule would you like to see?"

- Admin: "Show Bikash Sir's schedule tomorrow."
  → search_teachers("Bikash")
  → teacher_schedule(teacher_id=<resolved_id>, schedule_date=<tomorrow>)

- Admin: "Show M[r]inmoy Sir's schedule tomorrow."
  → search_teachers("Mrinmoy")
  → teacher_schedule(teacher_id=<resolved_id>, schedule_date=<tomorrow>).
"""

class AgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        access_token = self._get_token(request)

        agent = get_agent(access_token=access_token)

        try:
            user_query = request.data["message"]

        except KeyError:
            return StreamingHttpResponse(
                self._event(
                    "error",
                    {"message": "message is required"},
                ),
                content_type="text/event-stream",
                status=400,
            )

        config = {
            "configurable": {
                "thread_id": str(request.user.id)
            }
        }

        async def event_stream():

            async for event in agent.astream_events(
                {
                    "messages": [
                        SystemMessage(content=system_message),
                        HumanMessage(content=user_query),
                    ]
                },
                config=config,
                version="v2",
            ):

                event_name = event["event"]

                if event_name == "on_tool_start":

                    yield self._event(
                        "tool_start",
                        {
                            "tool": event["name"],
                        },
                    )

                elif event_name == "on_tool_end":

                    yield self._event(
                        "tool_end",
                        {
                            "tool": event["name"],
                        },
                    )

                elif event_name == "on_chat_model_stream":

                    chunk = event["data"]["chunk"]
                    content = chunk.content

                    if content:
                        yield self._event(
                            "token",
                            {
                                "content": content,
                            },
                        )

            yield self._event(
                "done",
                {
                    "status": "completed"
                },
            )

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )

        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"

        return response

    @staticmethod
    def _event(event_type, data):
        return (
            f"event: {event_type}\n"
            f"data: {json.dumps(data)}\n\n"
        )

    @staticmethod
    def _get_token(request):
        auth_header = request.headers.get(
            "Authorization",
            "",
        )

        return auth_header.replace("Bearer ", "")