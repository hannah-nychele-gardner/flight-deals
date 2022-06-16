
from dotenv import load_dotenv
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


class FlightSearch:
    def __init__(self):
        """Interfaces with kiwi api"""
        load_dotenv("C:/Users/hanna/OneDrive/Documents/Learning/EnvironmentVariables/.env")
        self.kiwi_api_key = os.getenv("KIWI_API_KEY")
        self.kiwi_endpoint = "https://tequila-api.kiwi.com"
        self.headers = {
            "apikey": self.kiwi_api_key
        }

    def get_iata(self, location):
        """Gets the iata code for a given city"""
        iata_endpoint = f"{self.kiwi_endpoint}/locations/query"
        query = {
            "term": location,
            "location_types": "city"
        }
        response = requests.get(url=iata_endpoint, params=query, headers=self.headers)
        return response.json()["locations"][0]["code"]

    def find_cheapest_flight(self, departure_iata_code, destination_iata_code):
        """Finds the cheapest round trip tickets to a given city departing any time between tomorrow and six months
         from tomorrow. Trip will be between 7 and 14 days in length."""
        tomorrow = datetime.now() + relativedelta(days=+1)
        formatted_tomorrow = tomorrow.strftime("%d/%m/%Y")
        six_months_from_tomorrow = tomorrow + relativedelta(months=+6)
        formatted_six_months_from_tomorrow = six_months_from_tomorrow.strftime("%d/%m/%Y")

        cheap_flight_endpoint = f"{self.kiwi_endpoint}/v2/search"
        query = {
            "fly_from": departure_iata_code,
            "fly_to": destination_iata_code,
            "date_from": formatted_tomorrow,
            "date_to": formatted_six_months_from_tomorrow,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "curr": "USD",
        }
        response = requests.get(url=cheap_flight_endpoint, params=query, headers=self.headers)
        return response.json()["data"][0]
