import logging

from django.http import HttpRequest, HttpResponse


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.logger.info(f'{request.META.get("REMOTE_ADDR")} {request.META.get("HTTP_X_FORWARDED_FOR")} {request.user}')
        request_body = str(request.body, 'utf-8').replace('\n', '')
        self.logger.info(f'Request: {request.method} {request.path} {request.headers} {request_body}')
        response: HttpResponse = self.get_response(request)
        response_body = str(response.content, 'utf-8').replace('\n', '')
        self.logger.info(f'Response: {response.status_code} {response.headers} {response_body}')
        return response
