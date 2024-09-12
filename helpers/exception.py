from django.http import JsonResponse
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse
from rest_framework.exceptions import (MethodNotAllowed,
                                       NotAcceptable,
                                       NotAuthenticated,
                                       NotFound,
                                       PermissionDenied,
                                       ValidationError,
                                       UnsupportedMediaType,
                                       Throttled,
                                       APIException)


class StandardExceptionFormatter(ExceptionFormatter):
    """
    Custom Standardized Response formatter.
    """

    def format_error_response(self, error_response: ErrorResponse):
        """Beautify the error response."""

        e = error_response.errors[0]
        e_detl = f"{e.detail.strip('.')}"
        e_attr = f": {e.attr}" if e.attr else ""

        return {
            'status': self.exc.status_code,
            'success': False,
            'message': f"{e_detl}{e_attr}",
            'error': error_response.type,
        }


class HttpError(APIException):
    """
    Custom HTTP error class to be raised on which will be caught by Standardized Response.
    """

    def __init__(self, status_code: int, detail: str):
        """
        Should not be used directly. Use the attributes instead.

        Example:
        >>> raise HttpError._400_("Bad Request")
        >>> raise HttpError._404_("Not Found")
        """

        assert self.__class__ != HttpError, "HttpError class should not be used directly."

    _400_ = ValidationError
    _401_ = NotAuthenticated
    _403_ = PermissionDenied
    _404_ = NotFound
    _405_ = MethodNotAllowed
    _406_ = NotAcceptable
    _415_ = UnsupportedMediaType
    _429_ = Throttled


def handler_404(request, exception):
    return JsonResponse(
        {
            'status': 404,
            'success': False,
            'message': f"Resource {request.path} was not found on the server.",
            'error': "invalid_url",
        }, status=404
    )


def handler_500(request):
    return JsonResponse(
        {
            'status': 500,
            'success': False,
            'message': "Internal Server Error.",
            'error': "internal_server_error",
        }, status=500
    )
