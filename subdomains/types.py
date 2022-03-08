from typing import Set, Tuple


class Record:
    identifier = None
    name: str
    ttl: int
    r_class: str = 'IN'
    r_type: str
    data: str

    def __init__(self, name: str, ttl: int, record_type: str, data: str):
        self.name = name
        self.ttl = ttl
        if record_type in self.get_available_types():
            self.r_type = record_type
        self.data = data

    def __str__(self):
        return f'{self.name} {self.ttl} {self.r_class} {self.r_type} {self.data}'

    @staticmethod
    def get_available_types() -> Set[str]:
        return {'A', 'NS', 'CNAME', 'MX', 'TXT', 'AAAA', 'SRV'}


class ARecord(Record):  # a host address
    def __init__(self, name: str, ttl: int, ip_address: str):
        super().__init__(name, ttl, 'A', ip_address)


class NsRecord(Record):  # an authoritative name server
    def __init__(self, name: str, ttl: int, name_server: str):
        super().__init__(name, ttl, 'NS', name_server)


class CnameRecord(Record):  # the canonical name for an alias
    def __init__(self, name: str, ttl: int, alias: str):
        super().__init__(name, ttl, 'CNAME', alias)


class MxRecord(Record):  # mail exchange
    def __init__(self, name: str, ttl: int, mail_server: str, priority: int):
        super().__init__(name, ttl, 'MX', f'{priority} {mail_server}')
        self.mail_server = mail_server
        self.priority = priority

    def get_data(self) -> Tuple[str, str]:
        priority, mail_server = self.data.split(' ')
        return mail_server, priority

    def set_data(self, mail_server: str, priority: int):
        self.data = f'{priority} {mail_server}'


class TxtRecord(Record):  # text strings
    def __init__(self, name: str, ttl: int, value: str):
        super().__init__(name, ttl, 'TXT', value)


class AaaaRecord(ARecord):  # IP6 Address
    def __init__(self, name: str, ttl: int, ip_address: str):
        super().__init__(name, ttl, ip_address)
        self.record_type = 'AAAA'


class SrvRecord(Record):  # Server Selection
    def __init__(self, name: str, ttl: int, service: str, protocol: str,
                 priority: int, weight: int, port: int, server_host_name: str):
        super().__init__(f'{service}.{protocol}.{name}', ttl, 'SRV', f'{priority} {weight} {port} {server_host_name}')

    def get_name(self) -> Tuple[str, str, str]:
        names = self.name.split('.')
        service = names[0]
        protocol = names[1]
        name = ''.join(names[2:])
        return name, service, protocol

    def set_name(self, name: str, service: str, protocol: str):
        self.name = f'{service}.{protocol}.{name}'
