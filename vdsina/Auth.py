import json
import os
import requests
from .common import check_response


class Auth:
    """
    A class for authorization at vdsina.ru API

    Agrs:
        api_url (str): Provider API server URL
    """
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = self.get_session()

    def get_session(self):
        def check_auth() -> str | None:
            token = os.getenv('VDSINA_TOKEN')
            login = os.getenv('VDSINA_LOGIN')
            password = os.getenv('VDSINA_PASSWORD')
            if token:
                return token
            elif login and password:
                return self.get_token(login, password)
            else:
                print(f'You should set the environment variables TOKEN or LOGIN and PASSWORD')
                exit(1)
        session = requests.Session()
        session.headers.update({'Content-Type': 'application/json'})
        session.headers.update({'Authorization': check_auth()})
        return session

    def get_token(self, login, password) -> str:
        url = f'{self.api_url}auth'
        payload = json.dumps({'email': login, 'password': password})
        session = requests.Session()
        response = session.post(url, data=payload)
        return check_response(response)['token']




