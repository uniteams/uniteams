from _datetime import datetime, timedelta
import time
import jwt
from uniteams import settings

from django.contrib.auth.models import AbstractUser
from django.db import models


class UniteamsUser(AbstractUser):

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt_exp = time.mktime((datetime.now() + timedelta(days=settings.EXP_TOKEN)).timetuple())

        token = jwt.encode({
            'user_id': self.pk,
            'exp': int(dt_exp),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Company(models.Model):
    company_name = models.CharField(max_length=255)
