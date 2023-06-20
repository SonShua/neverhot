from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        # empty string email is converted to None in managers.py
        user = User.objects.create_user(username="usher", email="", password="foo")
        self.assertEqual(user.username, "usher")
        self.assertIsNone(user.email)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="", email="", password="foo")
        User.objects.create_user(username="liljohn", email=None, password="getlow")
