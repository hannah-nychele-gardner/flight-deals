import os
from dotenv import load_dotenv
from twilio.rest import Client


class NotificationManager:
    def __init__(self):
        """Interfaces with twilio api"""
        load_dotenv("C:/Users/hanna/OneDrive/Documents/Learning/EnvironmentVariables/.env")
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.sending_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.receiving_number = os.getenv("PERSONAL_PHONE_NUMBER")

    def send_message(self, message_text):
        """Sends text message"""
        client = Client(self.account_sid, self.auth_token)
        client.messages.create(
            body=message_text,
            from_=self.sending_number,
            to=self.receiving_number
        )