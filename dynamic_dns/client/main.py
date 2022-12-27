import argparse

from dynamic_dns.client.client import DynamicDnsClient

host = {
    'prod': 'https://subshorts.com',
    'dev': 'http://localhost:8080',
}

endpoint = 'dynamic-dns'

target = 'prod'


def main(args: argparse.Namespace) -> None:
    token = args.token
    client = DynamicDnsClient(token, host[target], endpoint)
    print(client.retrieve())
    print(client.update())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('token')
    main(parser.parse_args())
