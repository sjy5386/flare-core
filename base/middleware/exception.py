import uuid

from django.http import HttpRequest, HttpResponse

from .base import BaseMiddleware


class ExceptionHandlingMiddleware(BaseMiddleware):
    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        debug_uuid = uuid.uuid4()
        self.logger.info(f'Debug UUID: {debug_uuid}')
        return
