from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    alphanumeric = RegexValidator(
        r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
    )
    username = models.CharField(
        max_length=50, blank=False, null=False, unique=True, validators=[alphanumeric]
    )
    email = models.EmailField(null=True, blank=True, unique=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def clean_email(self):
        return self.cleaned_data["email"] or None
