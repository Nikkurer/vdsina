import json
import os
import requests
from .common import check_response


class Auth:
    """
    A class for authorization
    """
    def __init__(self, api_url):
        self.api_url = api_url
        self.session = self.get_session()

    def get_session(self):
        def check_auth() -> str | None:
            token = os.getenv('TOKEN')
            login = os.getenv('LOGIN')
            password = os.getenv('PASSWORD')
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




