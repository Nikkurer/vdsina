import json
from .Service import Service
from .Objects import Server, SshKey, IsoImage
from .common import check_response
from email_validator import validate_email, EmailNotValidError


class Account(Service):
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
    servers = []
    ssh_keys = []
    iso_images = []
    templates = None
    datacenters = None
    server_groups = None
    server_plans = []

    def __init__(self, api_url: str):
        """
        Inits Account with api_url (str) as provider API server URL
        Args:
            api_url (str): API server URL
        """
        super().__init__(api_url)
        self.account = self._get_parameter('account')
        self.templates = self._get_parameter('template')
        self.limits = self._get_parameter('account.limit')
        self.datacenters = self._get_parameter('datacenter')
        self.balance = self._get_parameter('account.balance')
        self.server_groups = self._get_parameter('server-group')
        self._get_servers()
        self._get_ssh_keys()
        self._get_iso_images()
        self._get_sever_plans()

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

    def _get_sever_plans(self):
        """
        Get server plans for a specific server group
        Returns:
            None
        Raises:
            HTTPError: If http status code not 20X
        """
        for server_group in self.server_groups:
            url = f'{self.api_url}server-plan/{server_group["id"]}'
            response = self.session.get(url)
            self.server_plans[server_group["id"]] = check_response(response)

    def _get_iso_images(self):
        """
        Get available ISO images
        Returns:
            List of available ISO images
        Raises:
            HTTPError: If http status code not 20X
        """
        iso_images = self._get_parameter('iso')
        if iso_images:
            for iso_image in iso_images:
                self.iso_images.append(IsoImage(self._get_parameter('iso', iso_image['id'])))

    def _get_ssh_keys(self):
        """
        Get ssh keys list
        Returns:
            List of ssh keys for account
        Raises:
            HTTPError: If http status code not 20X
        """
        self.ssh_keys = []
        ssh_keys = self._get_parameter('ssh-key')
        for ssh_key in ssh_keys:
            self.ssh_keys.append(SshKey(self._get_parameter('ssh-key', ssh_key['id'])))

    def _get_servers(self):
        self.servers = []
        servers = self._get_parameter('server')
        for server in servers:
            self.servers.append(Server(self._get_parameter('server', server['id'])))

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
        self._get_ssh_keys()
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
        self._get_ssh_keys()
        return check_response(response)

    # def create_server(self, server: Server):
