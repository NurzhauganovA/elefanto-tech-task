from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from account.managers import UserManager


phone_number_validator = RegexValidator(
    regex=r'^\+7\d{10}$',
    message='Phone number must start with +7 and contain 10 digits.',
    code='invalid_phone_number'
)

password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',
    message='Password must contain at least 8 characters, at least one uppercase letter, one lowercase letter, and one digit.',
    code='invalid_password'
)


class User(PermissionsMixin, AbstractBaseUser):
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200, validators=[password_validator])
    mobile_phone = models.CharField(max_length=25, blank=True, null=True, validators=[phone_number_validator])
    birth_date = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name', 'password']

    def __str__(self):
        return self.mobile_phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
