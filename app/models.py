from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username or not phone_number:
            raise ValueError("Username and phone number are required")
        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password or phone_number)  # default password is phone
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None):
        user = self.create_user(username, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username
