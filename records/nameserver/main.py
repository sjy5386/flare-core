import argparse

from dnslib.server import DNSServer
from dnslib.zoneresolver import ZoneResolver


def main(args: argparse.Namespace) -> None:
    zone = '\n'.join((
        'example.com 300 IN NS ns.example.com',
        'example.com 300 IN A 127.0.0.1',
        'example.com 300 IN AAAA ::1',
    ))
    resolver = ZoneResolver(zone, False)
    dns_server = DNSServer(resolver, port=args.port)
    print(f'listen {args.port}')
    dns_server.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=53)
    main(parser.parse_args())
