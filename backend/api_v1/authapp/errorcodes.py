from django.utils.translation import ugettext_lazy as _
from rest_framework import status

ERR_WRONG_LOGIN_OR_PASSWRD = {
    'code': 100001,
    'detail': _('Wrong login or password'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_LOGIN_ALREADY_EXIST = {
    'code': 100002,
    'detail': _('Login already exist'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_WRONG_LOGIN = {
    'code': 100003,
    'detail': _('Wrong login'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_WRONG_PASSWORD = {
    'code': 100004,
    'detail': _('Wrong password'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_WRONG_TOKEN = {
    'code': 100005,
    'detail': _('Authentication credentials were not provided'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_INVALID_TOKEN = {
    'code': 100006,
    'detail': _('Invalid authentication. Could not decode token.'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_TOKEN_OUT_OF_DATE = {
    'code': 100007,
    'detail': _('Invalid authentication. Token is out of date.'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_TOKEN_NOT_SEARCH_USER = {
    'code': 100010,
    'detail': _('No user matching this token was found.'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_TOKEN_USER_NOT_ACTIVE = {
    'code': 100011,
    'detail': _('This user has been deactivated.'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_NO_GROUP_ID_IN_QUERY = {
    'code': 100012,
    'detail': _('No correct group_id param in query'),
    'status': status.HTTP_404_NOT_FOUND
}

ERR_NO_RIGHTS_FOR_ACTION = {
    'code': 100013,
    'detail': _('No rights for action'),
    'status': status.HTTP_403_FORBIDDEN
}

ERR_USER_ALREADY_IN_GROUP = {
    'code': 100014,
    'detail': _('User already in group'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_USER_NOT_FOUND = {
    'code': 100015,
    'detail': _('User not found'),
    'status': status.HTTP_404_NOT_FOUND
}

ERR_USER_ALREADY_IN_CONTACT_LIST = {
    'code': 100016,
    'detail': _('User already in contacts'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_USER_IS_NOT_ACTIVE = {
    'code': 100017,
    'detail': _('This account is inactive'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_WRONG_ACTIVATION_KEY = {
    'code': 100018,
    'detail': _('User activation failed - wrong email or activation key'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_USER_ALREADY_ACTIVATED = {
    'code': 100019,
    'detail': _('User activation failed - already activated'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_ACTIVATION_KEY_EXPIRED = {
    'code': 100020,
    'detail': _('User activation failed - activation key is expired'),
    'status': status.HTTP_400_BAD_REQUEST
}

ERR_COMPANY_DOES_NOT_EXIST = {
    'code': 100030,
    'detail': _('No company with the name found.'),
    'status': status.HTTP_404_NOT_FOUND
}