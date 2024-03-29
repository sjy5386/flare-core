import os

from django.core.management.utils import get_random_secret_key


def get_secret_key():
    filename = 'SECRET_KEY'
    if os.path.isfile(filename):
        f = open(filename, 'r')
        line = f.readline()
        f.close()
        return line
    else:
        random_secret_key = get_random_secret_key()
        f = open(filename, 'w')
        f.write(random_secret_key)
        f.close()
        return random_secret_key


def get_allowed_hosts():
    return tuple(map(lambda x: x.strip(), os.environ.get('ALLOWED_HOSTS', '*').split(',')))


def get_csrf_trusted_origins():
    filename = 'CSRF_TRUSTED_ORIGINS'
    if os.path.isfile(filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        return tuple(map(lambda x: x.strip(), lines))
    return (
        'http://localhost:8000',
    )
