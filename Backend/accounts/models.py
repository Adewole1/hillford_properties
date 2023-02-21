from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

from authemail.models import EmailUserManager, EmailAbstractUser

from .managers import CustomUserManager


class CustomUser(EmailAbstractUser):
    # first_name = models.CharField(_("First name"), max_length=50)
    # last_name = models.CharField(_("Last name"), max_length=50)
    phone_number = PhoneNumberField(region='NG')
    username = models.CharField(max_length=40, unique=False, default='')
    # email = models.EmailField(_('email address'), unique=True)
    # is_staff = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(default=timezone.now)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    objects = EmailUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('All Users')
        # abstract = True


class Staff(CustomUser):

    positions = [
        ('CEO', 'Chief Executive Officer'),
        ('realtor', 'Realtor'),
        ('staff', 'Staff')
    ]

    position = models.CharField(_("Position"), max_length=50, choices=positions)
    slug = AutoSlugField(populate_from=f'get_user', unique=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_user(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = _('Staff')
        verbose_name_plural = _('Staff')
        # abstract = True
