import os
from dotenv import load_dotenv
import requests


class DataManager:
    def __init__(self):
        """Interfaces with sheety api"""
        load_dotenv("C:/Users/hanna/OneDrive/Documents/Learning/EnvironmentVariables/.env")
        self.sheety_username = os.getenv("SHEETY_USERNAME")
        self.sheety_password = os.getenv("SHEETY_PASSWORD")
        self.sheety_endpoint = "https://api.sheety.co/9a965fe7a0d51286397080fabe679205/flightDeals/prices"

    def get_rows(self):
        """Returns flight information from google sheet"""
        response = requests.get(url=self.sheety_endpoint, auth=(self.sheety_username, self.sheety_password))
        return response.json()

    def add_iata(self, object_id, iata):
        """Adds the iata code for rows in google sheet for which it is missing"""
        row_endpoint = f"{self.sheety_endpoint}/{object_id}"
        row_params = {
            "price": {
                "iataCode": iata
            }
        }
        response = requests.put(url=row_endpoint, json=row_params, auth=(self.sheety_username, self.sheety_password))
        return response.json()
