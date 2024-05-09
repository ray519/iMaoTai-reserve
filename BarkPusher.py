import sys
import time

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import config


class BarkPusher:
    def __init__(self):
        self.token_key_file_name = config.TOKEN_KEY_FILE_NAME
        self.device_token = config.DEVICE_TOKEN
        self.team_id = config.TEAM_ID
        self.auth_key_id = config.AUTH_KEY_ID
        self.topic = config.TOPIC
        self.apns_host_name = config.APNS_HOST_NAME
        # self.token = self.buildToken()

    def buildToken(self):
        # Current time in seconds since the Epoch
        jwt_issue_time = int(time.time())

        # Prepare the JWT Header
        jwt_header = {
            "alg": "ES256",
            "kid": self.auth_key_id
        }

        # Prepare the JWT Claims
        jwt_claims = {
            "iss": self.team_id,
            "iat": jwt_issue_time
        }

        # Load the private key for signing the JWT
        with open(self.token_key_file_name, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # 使用ES256算法对JWT进行签名
        encoded_jwt = jwt.encode(jwt_claims, private_key, algorithm='ES256', headers=jwt_header)

        # 构建认证Token
        authentication_token = encoded_jwt

        # 准备发送的推送数据
        payload = {
            'aps': {
                'alert': 'test'
            }
        }
        url = "https://{}/3/device/{}".format(self.apns_host_name, self.device_token)
        headers = {
                      'apns-topic': self.topic,
                      'apns-push-type': 'alert',
                      'authorization': f'bearer {authentication_token}'
                  },

        # 发送推送请求
        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        # 打印响应
        print(response.status_code)
        print(response.text)
