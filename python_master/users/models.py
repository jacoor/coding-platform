from typing import ClassVar

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user(self: "UserManager", email: str, password: str, **extra_fields: dict) -> "User":
        if not email:
            message: str = "Users must have an email address"
            raise ValueError(message)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self: "UserManager", email: str, password: str, **extra_fields: dict) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self: "UserManager", email: str, password: str, **extra_fields: dict) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            message: str = "Superuser must have is_staff=True."
            raise ValueError(message)
        if extra_fields.get("is_superuser") is not True:
            message: str = "Superuser must have is_superuser=True."
            raise ValueError(message)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    username: None = None
    email = models.EmailField(unique=True)
    last_activity = models.DateTimeField(auto_now_add=True, db_index=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []
