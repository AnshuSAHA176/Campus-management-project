from langchain.tools import tool
from .services import Services
from typing import Optional
import json
from .RAG.knowlagebase import knowledge_base


BASE_URL = "http://127.0.0.1:8000/"


def Tools(access_token):

    services = Services(base_url=BASE_URL, access_token=access_token)

    @tool
    def get_schedule(
        schedule_date: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ):
        """
        Get the authenticated user's class schedule.

        If no date or date range is provided, return today's schedule.

        Use `date` for a specific date.
        Use `date_from` and `date_to` for a date range.

        Dates must use YYYY-MM-DD format.
        """
        result = services.get_schedule(
            schedule_date=schedule_date,
            date_from=date_from,
            date_to=date_to,
        )

        if not result:
            return "No classes found for the requested date or date range."

        return json.dumps(result)

    @tool
    def get_available_rooms(
        schedule_date: str,
        start_time: str,
        end_time: str,
    ):
        """
        Find rooms available for a specific date and time range.

        schedule_date: Date in YYYY-MM-DD format.
        start_time: Start time in HH:MM:SS format.
        end_time: End time in HH:MM:SS format.

        Returns rooms that are active and not occupied by a scheduled
        class during the requested time.
        """

        result = services.get_avalable_rooms(
            schedule_date=schedule_date,
            start_time=start_time,
            end_time=end_time,
        )

        return json.dumps(result)

    @tool
    def check_schedule_conflict(
        schedule_date: str,
        start_time: str,
        end_time: str,
        teacher_id: Optional[int] = None,
        batch_id: Optional[int] = None,
        room_id: Optional[int] = None,
    ):
        """
        Check whether a proposed class schedule conflicts with
        an existing teacher, batch, or room schedule.

        The agent must resolve teacher, batch, and room names to
        their IDs using the search tools before calling this tool.

        If the user provides only a start time, the agent should
        assume a 1-hour class and calculate the end time.
        """

        if not schedule_date:
            return "schedule_date is required."

        if not start_time:
            return "start_time is required."

        if not end_time:
            return "end_time is required."

        if not teacher_id:
            return "teacher_id is required."

        if not batch_id:
            return "batch_id is required."

        if not room_id:
            return "room_id is required."

        result = services.check_schedule_conflict(
            schedule_date=schedule_date,
            start_time=start_time,
            end_time=end_time,
            teacher_id=teacher_id,
            batch_id=batch_id,
            room_id=room_id,
        )

        if not result:
            return "No conflict information was returned."

        return json.dumps(result, default=str)

    @tool
    def search_teachers(query: str):
        """
        Search for teachers by name or employee ID.

        Use this when the user mentions a teacher by name or employee ID
        and the teacher's database ID is needed for another operation.

        Example:
        search_teachers("Bikash")
        """

        result = services.search_teachers(query)

        if not result:
            return "No teacher found matching the search."

        return json.dumps(result, default=str)

    @tool
    def search_batches(query: str):
        """
        Search for batches by batch name.

        Use this when the user mentions a batch such as BCA-3B
        and the batch's database ID is needed.

        Example:
        search_batches("BCA-3B")
        """

        result = services.search_batches(query)

        if not result:
            return "No batch found matching the search."

        return json.dumps(result, default=str)

    @tool
    def search_rooms(query: str):
        """
        Search for rooms by room number or floor.

        Use this when the user mentions a room such as Room 301
        and the room's database ID is needed.

        Example:
        search_rooms("301")
        """

        result = services.search_rooms(query)

        if not result:
            return "No room found matching the search."

        return json.dumps(result, default=str)

    @tool
    def teacher_schedule(
        teacher_id: int | None,
        schedule_date: str,
    ):
        """
        Get a teacher's class schedule for a specific date.

        If the authenticated user is a teacher and asks for their own
        schedule, teacher_id can be None.

        If the user is an admin or another non-teacher and asks for a
        teacher's schedule, teacher_id is required. The agent must first
        use search_teachers to resolve the teacher's name to an ID.

        Never call this tool with teacher_id=None for an admin.

        Args:
            teacher_id:
                Teacher database ID. Can be None only for a teacher
                requesting their own schedule.

            schedule_date:
                Date in YYYY-MM-DD format.
        """

        if teacher_id is None:
            return (
                "A teacher name is required. "
                "Use search_teachers to find the teacher first."
            )

        result = services.teacher_schedule(
            teacher_id=teacher_id,
            schedule_date=schedule_date,
        )

        return json.dumps(result, default=str)

    @tool
    def find_available_rooms(
        schedule_date: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """
        Find rooms that are available for the requested date and time.

        If schedule_date is not provided, use today's date.
        Dates must use YYYY-MM-DD format.
        Times must use HH:MM:SS format.
        """
        result = services.room_avalable(
            schedule_date=schedule_date, start_time=start_time, end_time=end_time
        )

        return json.dumps(result, default=str)

    @tool
    def search_subjects(query: str):
        """
        Search for subjects by subject name or code.

        Use this when the user mentions a subject and its database ID
        is needed for another operation.

        Example:
        search_subjects("Data Structures")
        """

        result = services.search_subjects(query)

        if not result:
            return "No subject found matching the search."

        return json.dumps(result, default=str)
    @tool
    def knowledge_base_tool(user_query:str):
        """
    Search the campus knowledge base for relevant institutional information.

    Use this tool when the user asks about university rules, academic
    regulations, department information, procedures, policies, notices,
    courses, attendance, examinations, or other information that may
    exist in the uploaded campus documents.

    Args:
        user_query: The user's question or search query.

    Returns:
        A JSON string containing the most relevant document chunks,
        including document ID, page range, and chunk text.
    """

        result = knowledge_base(user_query=user_query)

        return json.dumps(result, default=str)



    return (
        get_schedule,
        get_available_rooms,
        check_schedule_conflict,
        search_teachers,
        search_batches,
        search_rooms,
        teacher_schedule,
        find_available_rooms,
        search_subjects,
        knowledge_base_tool,
    )
