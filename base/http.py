import ipaddress

from django.http import HttpRequest


def get_remote_ip_address(request: HttpRequest) -> str:
    return list(map(lambda x: x.strip(),
                    request.META.get('HTTP_X_FORWARDED_FOR',
                                     request.META.get('REMOTE_ADDR')).split(',')))[0]


def is_private_ip_address(ip_address: str) -> bool:
    return any(ipaddress.ip_address(ip_address) in network for network in map(ipaddress.ip_network, (
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
    )))
