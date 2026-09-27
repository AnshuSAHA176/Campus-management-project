from datetime import date
import requests


class Services:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def get_schedule(
    self,
    schedule_date=None,
    date_from=None,
    date_to=None,
    ):
        if not schedule_date and not date_from and not date_to:
            schedule_date = date.today().isoformat()

        params = {}

        if schedule_date:
            params["date"] = schedule_date

        if date_from:
            params["date_from"] = date_from

        if date_to:
            params["date_to"] = date_to

        response = requests.get(
            f"{self.base_url}scheduling/tools/",
            headers=self._headers(),
            params=params,
        )

        

        return response.json()
    def get_avalable_rooms(
    self,
    schedule_date=None,
    start_time=None,
    end_time=None,
    ):
        if not schedule_date and not start_time and not end_time:
            schedule_date = date.today().isoformat()

        params = {}

        if schedule_date:
            params["date"] = schedule_date

        if start_time:
            params["start_time"] = start_time


        if end_time:
            params["end_time"] = end_time

        response = requests.get(
            f"{self.base_url}scheduling/available-rooms/",
            headers=self._headers(),
            params=params,
        )

        response.raise_for_status()

        return response.json()

