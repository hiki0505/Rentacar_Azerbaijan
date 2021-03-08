from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, username, phone, password, is_company, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        # if not email:
        #     raise ValueError('The Email must be set')
        # email = self.normalize_email(email)
        self.phone = phone
        extra_fields.setdefault('is_active', False)
        user = self.model(username=username, phone=phone, is_company=is_company, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone, password, username='admin', is_company=False, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, phone, password, is_company, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=False, default='anon')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+994505353535'. Up to 15 digits "
                                         "allowed.")
    phone = models.CharField('phone number', validators=[phone_regex], max_length=15,
                             unique=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    is_company = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+994505353535'. Up to 15 digits "
                                         "allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validdate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
