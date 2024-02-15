import logging
from abc import ABCMeta

from django.http import HttpRequest, HttpResponse


class BaseMiddleware(metaclass=ABCMeta):
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        pass
