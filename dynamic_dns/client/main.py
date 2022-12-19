import argparse

import requests

host = {
    'prod': 'https://subshorts.com',
    'dev': 'http://localhost:8080',
}

endpoint = 'dynamic-dns'

target = 'prod'


def retrieve(token: str) -> str:
    return requests.get(f'{host[target]}/{endpoint}/{token}/').text


def update(token: str) -> str:
    return requests.post(f'{host[target]}/{endpoint}/{token}/').text


def main(args: argparse.Namespace) -> None:
    token = args.token
    print(retrieve(token))
    print(update(token))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('token')
    main(parser.parse_args())
