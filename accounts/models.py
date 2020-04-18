from django.db import models
from django.contrib import auth
# Create your models here.
# https://docs.djangoproject.com/en/3.0/ref/contrib/auth/--
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return "@{}".format(self.username)

