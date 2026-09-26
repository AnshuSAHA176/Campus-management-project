from langchain.tools import tool
from .services import Services
from typing import Optional
import json 


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

    return get_schedule
