import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('twillio_account_sid')
auth_token = os.getenv('twillio_auth_token')
client = Client(account_sid, auth_token)


def send_message(message, message_from='+12762125643', message_to='+918106918896'):
    message = client.messages.create(
        body=message,
        from_=message_from,
        to=message_to
    )
    print(message.sid)


if __name__ == "__main__":
    send_message("Plant disease")
