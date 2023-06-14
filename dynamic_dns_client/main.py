import argparse

from dynamic_dns_client.client import DynamicDnsClient


def main(args: argparse.Namespace) -> None:
    token = args.token
    host = args.host
    client = DynamicDnsClient(token, host)
    print(client.retrieve())
    print(client.update())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='Your authentication token.')
    parser.add_argument('--host', type=str, default='https://subshorts.com')
    main(parser.parse_args())
