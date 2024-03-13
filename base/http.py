import ipaddress

from django.http import HttpRequest
from django.test import TestCase


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


class Test(TestCase):
    def test_get_remote_ip_address(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.assertEqual('127.0.0.1', get_remote_ip_address(request))

    def test_is_private_ip_address(self):
        # class A
        self.assertFalse(is_private_ip_address('9.0.0.254'))
        self.assertTrue(is_private_ip_address('10.0.0.1'))
        self.assertTrue(is_private_ip_address('10.255.255.254'))
        self.assertFalse(is_private_ip_address('11.0.0.1'))
        # class B
        self.assertFalse(is_private_ip_address('172.15.255.254'))
        self.assertTrue(is_private_ip_address('172.16.0.1'))
        self.assertTrue(is_private_ip_address('172.31.255.254'))
        self.assertFalse(is_private_ip_address('172.32.0.1'))
        # class C
        self.assertFalse(is_private_ip_address('192.167.255.254'))
        self.assertTrue(is_private_ip_address('192.168.0.1'))
        self.assertTrue(is_private_ip_address('192.168.255.254'))
        self.assertFalse(is_private_ip_address('192.169.0.1'))
