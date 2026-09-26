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

    def get_today_schedule(self):
        responce = requests.get(url=f'{self.base_url}scheduling/'
                                , headers=self._headers())
        responce.raise_for_status()
        return responce.json()