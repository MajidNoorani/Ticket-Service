from django.db import models  # noqa
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, name, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address.")
        if not name:
            raise ValueError("User must have name.")
        user = self.model(email=self.normalize_email(email),
                          name=name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # 'using' makes it robust to use 2 databases

        return user

    def create_superuser(self, email, name='admin', password=None):
        """Create, save and return a new superuser."""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # The field that is used for authentication
