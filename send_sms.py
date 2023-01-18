import requests
from get_name import name
from get_last_name import last_name
from get_email import email
from get_phone import phone
from get_api_key import api_key

# message = f"Hi {name} {last_name}, your email is {email} {phone}"

# payload = {"to_phone": phone, "message": message, "api_key": api_key}

# r = requests.post('https://fatsms.com/send-sms', payload)


def send_sms(code):
    message = code

    payload = {"to_phone": phone, "message": message, "api_key": api_key}

    r = requests.post('https://fatsms.com/send-sms', payload)

# print(r)
# print(r.text)
# print(message)
