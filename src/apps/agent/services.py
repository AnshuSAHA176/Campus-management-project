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

    def check_schedule_conflict(
        self,
        schedule_date,
        start_time,
        end_time,
        teacher_id=None,
        batch_id=None,
        room_id=None,
    ):
        params = {
            "date": schedule_date,
            "start_time": start_time,
            "end_time": end_time,
        }

        if teacher_id:
            params["teacher_id"] = teacher_id

        if batch_id:
            params["batch_id"] = batch_id

        if room_id:
            params["room_id"] = room_id

        response = requests.get(
            f"{self.base_url}scheduling/conflict/",
            headers=self._headers(),
            params=params,
        )

        response.raise_for_status()

        return response.json()

    def search_teachers(self, query):
        response = requests.get(
            f"{self.base_url}teacher_search/",
            headers=self._headers(),
            params={"q": query},
        )

        response.raise_for_status()

        return response.json()

    def search_batches(self, query):
        response = requests.get(
            f"{self.base_url}api/batches/search/",
            headers=self._headers(),
            params={"q": query},
        )

        response.raise_for_status()

        return response.json()

    def search_rooms(self, query):
        response = requests.get(
            f"{self.base_url}rooms/search/",
            headers=self._headers(),
            params={"q": query},
        )

        response.raise_for_status()

        return response.json()

    def teacher_schedule(self, teacher_id, schedule_date):
        params = {
            "date": schedule_date,
        }

        if teacher_id is not None:
            params["teacher_id"] = teacher_id

        response = requests.get(
            f"{self.base_url}scheduling/teacher-schedule/",
            headers=self._headers(),
            params=params,
        )

        if response.status_code == 400:
            return response.json()

        response.raise_for_status()

        return response.json()

    def room_avalable(self, schedule_date, start_time, end_time):
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
            f"{self.base_url}rooms/avalable/",
            headers=self._headers(),
            params=params,
        )

         if response.status_code == 400:
            return response.json()

         response.raise_for_status()

         return response.json()

    def search_subjects(self, query):
        response = requests.get(
            f"{self.base_url}api/subject/search/",
            headers=self._headers(),
            params={"q": query},
        )

        response.raise_for_status()

        return response.json()