from rest_framework.views import exception_handler


# Переопределим exception_handler
def core_exception_handler(exc, context):
    response = exception_handler(exc, context)

    handlers = {
        'ProfileDoesNotExist': _handle_generic_error,
        'ValidationError': _handle_generic_error,
        'AuthenticationFailed': _handle_generic_error,
        'UniteamsAuthException': _handle_generic_error,
    }

    # получим название класса
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'error': {
            'code': exc.get_codes(),
            'message': exc.detail
        }
    }

    return response