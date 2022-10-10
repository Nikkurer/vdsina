import json
import os
import requests
from .common import check_response


class Service:
    """
    The class for authorization at vdsina.ru API
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
        if response.ok:
            return check_response(response)['token']
        else:
            raise response.raise_for_status()

    def _get_parameter(self, endpoint: str, parameter_id: int = None):
        """
        Get parameter by its endpoint
        Args:
            endpoint (str): Endpoint name after API URL
            parameter_id (int): Optional. If parameter can get id
        Returns:
            Result of http request
        Raises:
            HTTPError: If http status code not 20X
        """
        url = f'{self.api_url}{endpoint}'
        if parameter_id:
            url = f'{url}/{parameter_id}'
        response = self.session.get(url)
        return check_response(response)

    def change_object(self, obj, parameter: str, value: str | dict = None):
        """
        Change parameter of object
        Args:
            obj (): Object to change
            parameter (str): Object parameter to change
            value (str|dict): New value of parameter
        Returns:

        """
        url = f'{self.api_url}{obj.endpoint}/{obj.id}'
        if isinstance(value, str):
            payload = json.dumps({parameter: value})
        elif isinstance(value, dict):
            payload = json.dumps(value)
        else:
            raise TypeError('value should be str or dict')
        response = self.session.put(url, payload)
        if check_response(response):
            obj.name = self._get_parameter(url)[parameter]
