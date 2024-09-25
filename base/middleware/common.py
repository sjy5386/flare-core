import threading
import uuid

from django.http import HttpRequest, HttpResponse

from .base import BaseMiddleware


class CommonMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        debug_id = uuid.uuid4().hex
        threading.current_thread().name = debug_id
        self.logger.info(f'Debug ID: {debug_id}')
        response: HttpResponse = self.get_response(request)
        response.headers['Flare-Debug-Id'] = debug_id
        return response
