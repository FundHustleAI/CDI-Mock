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



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

CATEGORY_CHOICES = [
    ('listening', 'Listening'),
    ('reading', 'Reading'),
    ('writing', 'Writing'),
]

class Test(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # A/B/C/D

    def __str__(self):
        return f"{self.category} - {self.question_text[:30]}"


class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listening_passed = models.BooleanField(default=False)
    reading_passed = models.BooleanField(default=False)
    writing_passed = models.BooleanField(default=False)
    seen_instructions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Progress"