import json
from .Auth import Auth
from .common import check_response
from email_validator import validate_email, EmailNotValidError


class Account(Auth):
    """VDSina account info
    The class for getting information about VDSina account and do some operations with it
    Args:
         api_url (str): Provider API server URL
    Attributes:
        account (dict): Account info
        limits (dict): Account limits
        balance (dict): Account balance
        server_groups (list): Account available server groups
    """
    limits = None
    balance = None
    account = None
    servers = None
    ssh_keys = []
    iso_images = []
    templates = None
    datacenters = None
    server_groups = None
    server_plans = {}

    def __init__(self, api_url: str):
        """
        Inits Account with api_url (str) as provider API server URL
        Args:
            api_url (str): API server URL
        """
        super().__init__(api_url)
        self.servers = self.get_parameter('server')
        self.account = self.get_parameter('account')
        self.templates = self.get_parameter('template')
        self.limits = self.get_parameter('account.limit')
        self.datacenters = self.get_parameter('datacenter')
        self.balance = self.get_parameter('account.balance')
        self.server_groups = self.get_parameter('server-group')
        self.get_ssh_keys()
        self.get_iso_images()
        for server_group in self.server_groups:
            self.get_sever_plans(server_group['id'])

    def __str__(self) -> str:
        account = f'Account:\n  Created: {self.account["created"]}\n  Forecast: {self.account["forecast"]}'
        balance = f'Balance:\n  Real: {self.balance["real"]}\n  Bonus: {self.balance["bonus"]}\n  Partner: {self.balance["partner"]}'
        limits = 'Limits:'
        for key in self.limits.keys():
            value = self.limits[key]
            if isinstance(value, dict):
                substr = f'{value["now"]}/{value["max"]}'
            elif isinstance(value, list | tuple | set):
                substr = f'{str(value)}'
            else:
                raise TypeError()
            limits = f'{limits}\n  {key.capitalize()}: {substr}'
        result = f'{account}\n{balance}\n{limits}'
        return result

    def get_parameter(self, endpoint: str, parameter_id: int = None):
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

    def get_sever_plans(self, sg_id: int) -> list:
        """
        Get server plans for a specific server group
        Args:
            sg_id (int): Server group id
        Returns:
            List of dictionaries with server plans
        Raises:
            HTTPError: If http status code not 20X
        """
        url = f'{self.api_url}server-plan/{sg_id}'
        response = self.session.get(url)
        self.server_plans[sg_id] = check_response(response)

    def get_iso_images(self) -> list:
        """
        Get available ISO images
        Returns:
            List of available ISO images
        Raises:
            HTTPError: If http status code not 20X
        """
        iso_images = self.get_parameter('iso')
        if iso_images:
            for iso_image in iso_images:
                self.ssh_keys.append(self.get_parameter('iso', iso_image['id']))

    def get_ssh_keys(self) -> list:
        """
        Get ssh keys list
        Returns:
            List of ssh keys for account
        Raises:
            HTTPError: If http status code not 20X
        """
        self.ssh_keys = []
        ssh_keys = self.get_parameter('ssh-key')
        for ssh_key in ssh_keys:
            self.ssh_keys.append(self.get_parameter('ssh-key', ssh_key['id']))

    def create_user(self, email: str):
        """
        Create user account
        Args:
            email (str): string with email
        Raises:
            HTTPError: If http status code not 20X
        """
        url = f'{self.api_url}register'
        # TODO: add partner code support
        try:
            validation = validate_email(email, check_deliverability=False)
            email = validation.email
            payload = json.dumps({"email": email})
            response = self.session.post(url, data=payload)
            return check_response(response)
        except EmailNotValidError as e:
            return str(e)

    def add_ssh_key(self, name: str, data: str):
        """
        Adds new ssh key
        Args:
            name (str): name of new ssh key
            data (str): public part of ssh key
        Raises:
            HTTPError: If http status code not 20X
        """
        url = f'{self.api_url}ssh-key'
        payload = json.dumps({'name': name, 'data': data})
        response = self.session.post(url, data=payload)
        self.get_ssh_keys()
        return check_response(response)

    def delete_ssh_key(self, ssh_key_id: int):
        """
         new ssh key
        Args:
            ssh_key_id (int): SSH key id
        Raises:
            HTTPError: If http status code not 20X
        """
        url = f'{self.api_url}ssh-key/{ssh_key_id}'
        response = self.session.delete(url)
        self.get_ssh_keys()
        return check_response(response)
