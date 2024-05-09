import json
import sys
import time

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import config


class BarkPusher:
    def __init__(self, phone):
        self.phone = phone
        device_map = config.BARK_DEVICE_TOKEN_CONFIG
        self.device_token = device_map.get(phone, config.DEFAULT_DEVICE_TOKEN)

    def bark(self):

        url = config.BARK_URL
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            "body": "token过期",
            "title": "{}i茅台token过期通知".format(self.phone),
            "device_key": self.device_token
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        print(response.text)
