from django.http import HttpRequest


def get_remote_ip_address(request: HttpRequest) -> str:
    return list(map(lambda x: x.strip(),
                    request.META.get('HTTP_X_FORWARDED_FOR',
                                     request.META.get('REMOTE_ADDR')).split(',')))[0]
