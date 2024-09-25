import logging
import threading
import uuid

from django.http import HttpRequest, HttpResponse

from .base import BaseMiddleware

log = logging.getLogger(__name__)


class CommonMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        debug_id = uuid.uuid4().hex
        threading.current_thread().name = debug_id
        log.info(f'Debug ID: {debug_id}')
        response: HttpResponse = self.get_response(request)
        response.headers['Flare-Debug-Id'] = debug_id
        return response
