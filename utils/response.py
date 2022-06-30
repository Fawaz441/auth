from distutils.log import error
from rest_framework.response import Response
from rest_framework.serializers import Serializer

SUCCESSFUL = 'success'
ERROR = 'failed'


class CustomResponse(Response):
    def __init__(self, code, status, message,
                 data=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(None, status=code)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        response = {'code': code, 'status': status, 'message': message}
        if data:
            response['data'] = data
        self.data = response
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
