from django.http import HttpRequest, HttpResponse

from .base import BaseMiddleware


class ExceptionHandlingMiddleware(BaseMiddleware):
    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        pass
