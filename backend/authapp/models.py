import hashlib
import random
from datetime import datetime, timedelta
import time
import jwt

from django.contrib.auth.models import AbstractUser, Group
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now

from phonenumber_field.modelfields import PhoneNumberField

from uniteams import settings


class UniteamsUser(AbstractUser):
    activation_key = models.CharField(max_length=255,
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

    @property
    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def generate_activation_key(self):
        self.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
        self.save()
        return self.activation_key

    def receive_activation_key(self):
        verify_link = f'{reverse("api_v1:auth:verify")}?email={self.email}&activation_key={self.activation_key}'
        email = EmailMessage(settings.EMAIL_ACTIVATION_KEY_SUBJECT,
                             f'{verify_link}',
                             f'{settings.EMAIL_HOST_USER}',
                             [self.email])
        return email.send()

    def create_team(self, team_name):
        try:
            team = UniteamsTeam(name=team_name, leader=self)
        except Exception as e:
            print(f'Could not create a company: {e}')
            return None
        else:
            team.members.add(self)
            team.save()

    def create_company(self, company_name):
        try:
            company = Company(company_name=company_name, owner=self, administrator=self)
        except Exception as e:
            print(f'Could not create a company: {e}')
            return None
        else:
            company.save()
            return company

    def __str__(self):
        return f'{self.username}'


class UserProfile(models.Model):
    user = models.OneToOneField('UniteamsUser',
                                related_name='profile',
                                on_delete=models.CASCADE,
                                null=True)
    first_name = models.CharField(max_length=255,
                                  blank=True)
    last_name = models.CharField(max_length=255,
                                 blank=True)
    avatar = models.ImageField(upload_to='users/avatars',
                               blank=True)
    phone = PhoneNumberField(blank=True)
    GENDERS = (('M', 'Male'),
               ('F', 'Female'))
    gender = models.CharField(max_length=16,
                              choices=GENDERS,
                              default='M',
                              blank=True)
    position = models.CharField(max_length=255,
                                blank=True)

    def __str__(self):
        return f'{self.user.username}\'s profile'


class UniteamsGroup(Group):
    pass


class UniteamsTeam(Group):
    leader = models.ForeignKey('UniteamsUser',
                               related_name='leader_of_groups',
                               on_delete=models.SET_NULL,
                               null=True)
    members = models.ManyToManyField('UniteamsUser',
                                     related_name='member_in_group',
                                     blank=True)

    def __str__(self):
        return f'{self.name} (leader: {self.leader.username})'


class OrgStruct(Group):
    children = models.ManyToManyField('self',
                                      related_name='child_of',
                                      blank=True)
    manager = models.ForeignKey('UniteamsUser',
                                related_name='manager_in',
                                on_delete=models.SET_NULL,
                                null=True)
    deputies = models.ManyToManyField('UniteamsUser',
                                      related_name='deputy_in',
                                      blank=True)
    participants = models.ManyToManyField('UniteamsUser',
                                          related_name='participating_in',
                                          blank=True)

    @property
    def parent(self):
        return self.child_of

    def change_manager(self, new_manager):
        self.manager = new_manager
        self.save()

    def __str__(self):
        return f'{self.of_company.name}{" -" if not self.parent else f" - {self.parent.name} - "}' \
            f'{self.name} (manager: {self.manager.username})'


class Company(models.Model):
    company_name = models.CharField(max_length=255,
                                    unique=True)
    org_struct = models.ForeignKey('OrgStruct',
                                   related_name='of_company',
                                   on_delete=models.CASCADE,
                                   null=True)
    owner = models.ForeignKey('UniteamsUser',
                              related_name='own_companies',
                              on_delete=models.SET_NULL,
                              null=True)
    administrator = models.ForeignKey('UniteamsUser',
                                      related_name='administrated_companies',
                                      on_delete=models.SET_NULL,
                                      null=True)

    employees = models.ManyToManyField('UniteamsUser',
                                       related_name='work_in_companies',
                                       blank=True
                                       )

    def change_owner(self, new_owner):
        self.owner = new_owner
        self.save()

    def change_admin(self, new_admin):
        self.administrator = new_admin
        self.save()

    def create_organisation_structure(self, name_of_structure):
        try:
            org_struct = OrgStruct(name=name_of_structure)
        except Exception as e:
            print(f'Could not to create org struct: {e}')
            return None
        else:
            org_struct.save()
            self.org_struct = org_struct
            return org_struct

    def __str__(self):
        return f'{self.company_name}{f"(owner: {self.owner.username}" if self.owner else "(no owner)"}'


@receiver(post_save, sender=UniteamsUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            user_profile = UserProfile(user=instance)
        except Exception as e:
            print(f'Could not create a user profile: {e}')
            return None
        else:
            user_profile.save()
            return user_profile
    else:
        return None
