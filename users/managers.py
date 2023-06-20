from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username or username is None:
            raise ValidationError("User must have username")
        if email is "":
            email = None
        # Making sure email is nulled to allow for blank emails in the db
        # alphanumeric = r"^[0-9a-zA-Z]*$"
        # if re.search(alphanumeric, username) == None:
        # raise ValidationError("Only alphanumeric allowed")
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_admin = True

        user.is_staff = True
        user.save(using=self._db)
        return user
