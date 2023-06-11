from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        try:
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                if not response.data.get('detail'):
                    non_fields_errors = response.data.get("non_field_errors")
                    if non_fields_errors and isinstance(non_fields_errors, list):
                        non_fields_errors = non_fields_errors[0]
                    # change default validation error response body,
                    # make it so front end can easily parse it
                    resp = {
                        'error_code': response.status_code,
                        'detail': non_fields_errors if non_fields_errors else 'Bad Request (invalid request body)',
                        'moreInfo': response.data
                    }
                    response.data = resp

            # add error code if not provided!
            if not response.data.get('error_code'):
                response.data['error_code'] = exc.default_code
        except Exception:
            pass

    return response


class CustomAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Conflict.')
    default_code = '500'

    def __init__(self, detail: str, status_code: status = None, error_code: int =None, more_info=None,
                 developer_message: str=None):
        """

        :param `str` detail: detail error message
        :param `int` status_code: Http Status Code for response
        :param `int` error_code: Error code, could be different from http status code, default is same
        :param more_info: more error information
        :param developer_message: detail error message for developers only
        """
        if status_code:
            self.status_code = status_code
        if status_code is not None and error_code is None:
            error_code = status_code

        detail = {
            "detail": detail,
        }
        if error_code is not None:
            detail["error_code"] = error_code
        if more_info:
            detail["more_info"] = more_info
        if developer_message:
            detail["developer_message"] = developer_message
        super(CustomAPIException, self).__init__(detail=detail, code=error_code)


class ConflictEmailEx(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Conflict Email')
    default_code = '409'


class ConflictPhoneEx(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Conflict Phone')
    default_code = '408'
