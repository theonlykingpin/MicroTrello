import secrets
import string
import uuid
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from trello.apps.users.sender import send_otp


class User(AbstractUser):
    pass


def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(4))


class OtpRequestQuerySet(models.QuerySet):

    def is_valid(self, data):
        # redis_otp = cache.get("otp")
        # try:
        #     if redis_otp['receiver'] == data['receiver'] and redis_otp['password'] == data['password']:
        #         print("OTP is valid")
        #         return True
        # except:
        #     print("OTP is invalid")
        #     return False
        self.delete_expired()
        return self.filter(
            request_id=data['request_id'],
            receiver=data['receiver'],
            password=data['password'],
            created__lt=timezone.now(),
            created__gt=timezone.now() - timedelta(seconds=120),
        ).exists()

    def delete_expired(self):
        self.filter(created__lt=timezone.now() - timedelta(seconds=120)).delete()


class OTPManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, data):
        return self.get_queryset().is_valid(data)

    def delete_expired(self):
        self.get_queryset().delete_expired()

    def generate(self, data):
        # new_otp = generate_otp()
        # print('new_otp------------>', new_otp)
        # redis_otp = {'receiver': data['receiver'], 'channel': data['channel'], 'password': new_otp}
        # cache.set("otp", redis_otp, timeout=120)
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp


class OTPRequest(models.Model):

    class OtpChannel(models.TextChoices):
        PHONE = 'Phone'
        EMAIL = 'E-Mail'

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()

    class Meta:
        verbose_name = 'OTP Request'
        verbose_name_plural = 'OTP Requests'
