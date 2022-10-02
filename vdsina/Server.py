import ipaddress


class Server:
    """
    Class to represent server information
    Args:
        server (dict): server representation from Account class
    """
    ip_addresses = []

    def __init__(self, server):
        self.rights = server['can']
        self.datacenter = server['datacenter']
        self.id = server['id']
        self.name = server['name']
        self.plan = server['server-plan']
        self.status = server['status']
        self.template = server['template']
        self.fqdn = server['host']
        self.get_ips(server['ip'])
        self.resources = server['data']
        self.server_plan = server['server-plan']
        self.server_group = server['server-group']
        self.template = server['template']
        self.datacenter = server['datacenter']
        self.ssh_key = server['ssh-key']
        self.bandwidth = server['bandwidth']

    def __str__(self) -> str:
        result = f'name: {self.name}\nfqdn: {self.fqdn}\nIP addresses:\n'
        for ip in self.ip_addresses:
            for key in ip.keys():
                result = f'{result}  {key}: {ip[key]}\n'
        result = f'{result}Resources:\n'
        for key in self.resources:
            resource = self.resources[key]
            result = f'{result} {key}: {resource["value"]} {resource["for"]}\n'
        return result

    def get_ips(self, ips_raw):
        for ip in ips_raw:
            self.ip_addresses.append(
                {'ip': ipaddress.IPv4Network(f'{ip["ip"]}/{ip["netmask"]}', False),
                 'gateway': ip['gateway'], 'mac': ip['mac']})
