from rest_framework.exceptions import APIException


class UniteamsAPIException(APIException):
    default_detail = 'undefined'
    default_code = 'undefined'

    def __init__(self, detail, code, status):
        super().__init__(detail=detail, code=code)
        self.status_code = status
