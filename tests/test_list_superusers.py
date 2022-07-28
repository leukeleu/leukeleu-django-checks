from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings


class TestListSuperusersNoAuth(TestCase):
    """Does nothing when django.contrib.auth is not in INSTALLED_APPS"""

    available_apps = [
        "leukeleu_django_checks",
    ]

    def test_no_user_model(self):
        out = StringIO()
        call_command("list_superusers", stdout=out, stderr=out)
        self.assertEqual(out.getvalue(), "")


@override_settings(AUTH_USER_MODEL="custom_users.NoSuperUser")
class TestListSuperusersCustomUserModel(TestCase):
    """Does nothing if AUTH_USER_MODEL does not have an is_superuser field"""

    def test_no_superuser_field(self):
        user_model = get_user_model()
        user_model.objects.create()

        out = StringIO()
        call_command("list_superusers", stdout=out, stderr=out)
        self.assertEqual(out.getvalue(), "")


class TestListSuperusersStandardUserModel(TestCase):
    def test_default_user_model(self):
        user_model = get_user_model()

        user_model.objects.create_superuser(
            username="admin",
        )
        user_model.objects.create_superuser(
            username="staff",
            email="staff.user@example.com",
        )
        john = user_model.objects.create_superuser(
            username="john",
            email="john.smith@example.com",
            first_name="John",
            last_name="Smith",
        )
        john.is_active = False
        john.save()

        out = StringIO()
        call_command("list_superusers", stdout=out, stderr=out)
        self.assertEqual(
            out.getvalue(),
            "\n".join(
                [
                    "+admin",  # Uses username field, if nothing else is available
                    "-John Smith",  # Prefers get_full_name
                    "+staff.user",  # Uses email field, removes domain part.
                    "",  # blank line
                ]
            ),
        )
