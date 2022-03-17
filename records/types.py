from typing import Dict


class BaseRecord:
    name: str
    ttl: int
    r_class: str = 'IN'
    r_type: str
    data: str

    def __init__(self, name: str, ttl: int, r_type: str, data: str):
        self.name = name
        self.ttl = ttl
        if r_type in self.get_available_types().keys():
            self.r_type = r_type
        self.data = data

    def __str__(self):
        return f'{self.name} {self.ttl} {self.r_class} {self.r_type} {self.data}'

    @staticmethod
    def get_available_types() -> Dict[str, str]:
        return {
            'A': 'a host address',
            'NS': 'an authoritative name server',
            'CNAME': 'the canonical name for an alias',
            'MX': 'mail exchange',
            'TXT': 'text strings',
            'AAAA': 'IP6 Address',
            'SRV': 'Server Selection'
        }


class Record(BaseRecord):
    identifier = None

    service: str
    protocol: str

    priority: int
    weight: int
    port: int

    target: str

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args)
        self.target = kwargs['target'] if 'target' in kwargs.keys() else self.data.split()[-1]
        if self.r_type in {'NS', 'CNAME', 'MX', 'SRV'} and self.target[-1] != '.':
            self.target += '.'
        if self.r_type == 'MX':
            priority = kwargs['priority'] if 'priority' in kwargs.keys() else 10
            self.set_data_mx(priority, self.target)
        elif self.r_type == 'SRV':
            service = '_http'
            protocol = '_tcp'
            if self.name[0] == '_':
                names = self.name.split('.')
                service = names[0]
                protocol = names[1]
                self.name = ''.join(names[2:])
            if 'service' in kwargs.keys():
                service = kwargs['service']
            if 'protocol' in kwargs.keys():
                protocol = kwargs['protocol']
            priority = kwargs['priority'] if 'priority' in kwargs.keys() else 10
            weight = kwargs['weight'] if 'weight' in kwargs.keys() else 100
            port = kwargs['port'] if 'port' in kwargs.keys() else 0
            self.set_name_srv(service, protocol, self.name)
            self.set_data_srv(priority, weight, port, self.target)
        if 'identifier' in kwargs.keys():
            self.identifier = kwargs['identifier']

    def get_name(self, suffix: str = None) -> str:
        name = self.name
        if self.r_type == 'SRV':
            name = ''.join(self.name.split('.')[2:])
        if suffix is not None:
            name += '.' + suffix
        return name

    def set_name_srv(self, service: str, protocol: str, name: str):
        self.service = service
        self.protocol = protocol
        self.name = f'{service}.{protocol}.{name}'

    def set_data_mx(self, priority: int, mail_server: str):
        if mail_server[-1] != '.':
            mail_server += '.'
        self.priority = priority
        self.target = mail_server
        self.data = f'{priority} {mail_server}'

    def set_data_srv(self, priority: int, weight: int, port: int, server_host_name: str):
        if server_host_name[-1] != '.':
            server_host_name += '.'
        self.priority = priority
        self.weight = weight
        self.port = port
        self.target = server_host_name
        self.data = f'{priority} {weight} {port} {server_host_name}'
