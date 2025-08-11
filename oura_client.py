import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class OuraClient:
    """
    Client API Oura Cloud v2 (endpoints usercollection/*).
    Permet de récupérer sommeil, readiness et activité.
    """
    API_BASE_URL = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, personal_access_token=None):
        self.token = personal_access_token or os.getenv("OURA_TOKEN")
        if not self.token:
            raise ValueError("Token OURA_TOKEN manquant dans .env")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _format_date(self, date_obj):
        return date_obj.strftime("%Y-%m-%d")

    def _request(self, endpoint, params=None):
        url = f"{self.API_BASE_URL}/{endpoint}"
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            return resp.json().get("data", [])
        print(f"Erreur Oura API {endpoint} : {resp.status_code} {resp.text}")
        return []

    def fetch_sleep_data_last_days(self, days=4):
        today = datetime.today()
        start_date = today - timedelta(days=days)
        params = {
            "start_date": self._format_date(start_date),
            "end_date": self._format_date(today)
        }
        return self._request("sleep", params=params)

    def fetch_readiness_data_last_days(self, days=4):
        today = datetime.today()
        start_date = today - timedelta(days=days)
        params = {
            "start_date": self._format_date(start_date),
            "end_date": self._format_date(today)
        }
        return self._request("readiness", params=params)

    def fetch_activity_data_last_days(self, days=4):
        today = datetime.today()
        start_date = today - timedelta(days=days)
        params = {
            "start_date": self._format_date(start_date),
            "end_date": self._format_date(today)
        }
        return self._request("daily_activity", params=params) 
