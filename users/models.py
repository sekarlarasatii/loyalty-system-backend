from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    points_balance = models.IntegerField(default=0)
    membership_status = models.CharField(
        max_length=10,
        choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')],
        default='Bronze'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        super().set_password(raw_password)

    def check_password(self, raw_password):
        return super().check_password(raw_password)

    def update_membership_status(self):
        if self.points_balance < 10000:
            self.membership_status = 'Bronze'
        elif 10000 <= self.points_balance < 50000:
            self.membership_status = 'Silver'
        else:
            self.membership_status = 'Gold'
        self.save()
