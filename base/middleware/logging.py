import logging
import traceback

from django.http import HttpRequest, HttpResponse

from .base import BaseMiddleware

log = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        remote_ip_address = list(map(lambda x: x.strip(),
                                     request.META.get('HTTP_X_FORWARDED_FOR',
                                                      request.META.get('REMOTE_ADDR')).split(',')))
        log.info(f'Request: {remote_ip_address} {request.method} {request.path}')
        log.info(f'Request Headers: {request.headers}')
        request_body = str(request.body, 'utf-8').replace('\n', '')
        log.info(f'Request Body: {request_body}')
        response: HttpResponse = self.get_response(request)
        log.info(f'User: {request.user}')
        log.info(f'Response: {response.status_code}')
        log.info(f'Response Headers: {response.headers}')
        response_body = self.get_response_body(response)
        log.info(f'Response Body: {response_body}')
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        log.error(''.join(traceback.format_exception(exception)))
        return

    @staticmethod
    def get_response_body(response: HttpResponse) -> str | bytes:
        try:
            return str(response.content, 'utf-8').replace('\n', '')
        except UnicodeDecodeError:
            return response.content
