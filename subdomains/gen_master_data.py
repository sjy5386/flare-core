from .models import ReservedName


def gen_master(apps, scheme_editor):
    reserved_names = ['co', 'com', 'example', 'go', 'gov', 'icann', 'ne', 'net', 'nic', 'or', 'org', 'whois', 'www']
    for reserved_name in reserved_names:
        ReservedName(name=reserved_name).save()
