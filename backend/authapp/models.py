import hashlib
import random
from _datetime import datetime, timedelta
import time
import jwt

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from phonenumber_field.modelfields import PhoneNumberField

from uniteams import settings


class UniteamsUser(AbstractUser):
    activation_key = models.CharField(max_length=128,
                                      blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=settings.EXP_ACTIVATION_KEY)))

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

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def activate(self):
        self.is_active = True
        self.save()

    def generate_activation_key(self):
        self.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
        self.save()
        return self.activation_key

class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='users/avatars',
                               blank=True)
    phone = PhoneNumberField(blank=True)


class Company(models.Model):
    company_name = models.CharField(max_length=255)
