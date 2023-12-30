import logging
import threading
import traceback
import uuid

from django.http import HttpRequest, HttpResponse


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        threading.current_thread().name = uuid.uuid4()
        remote_ip_address = list(map(lambda x: x.strip(),
                                     request.META.get('HTTP_X_FORWARDED_FOR',
                                                      request.META.get('REMOTE_ADDR')).split(',')))
        self.logger.info(f'Request: {remote_ip_address} {request.method} {request.path}')
        self.logger.info(f'Request Headers: {request.headers}')
        request_body = str(request.body, 'utf-8').replace('\n', '')
        self.logger.info(f'Request Body: {request_body}')
        response: HttpResponse = self.get_response(request)
        self.logger.info(f'User: {request.user}')
        self.logger.info(f'Response: {response.status_code}')
        self.logger.info(f'Response Headers: {response.headers}')
        response_body = self.get_response_body(response)
        self.logger.info(f'Response Body: {response_body}')
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        self.logger.error(''.join(traceback.format_exception(exception)))
        return

    @staticmethod
    def get_response_body(response: HttpResponse) -> str | bytes:
        try:
            return str(response.content, 'utf-8').replace('\n', '')
        except UnicodeDecodeError:
            return response.content
