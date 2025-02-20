from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings


class TestListStaffUsersNoAuth(TestCase):
    """Does nothing when django.contrib.auth is not in INSTALLED_APPS"""

    available_apps = [
        "leukeleu_django_checks",
    ]

    def test_no_user_model(self):
        out = StringIO()
        call_command("list_staff_users", stdout=out, stderr=out)
        self.assertEqual(out.getvalue(), "")


@override_settings(AUTH_USER_MODEL="custom_users.NoStaff")
class TestListStaffUsersCustomUserModel(TestCase):
    """Does nothing if AUTH_USER_MODEL does not have an is_staff field"""

    def test_no_staff_field(self):
        user_model = get_user_model()
        user_model.objects.create()

        out = StringIO()
        call_command("list_staff_users", stdout=out, stderr=out)
        self.assertEqual(out.getvalue(), "")


class TestListStaffUsersStandardUserModel(TestCase):
    def test_default_user_model(self):
        user_model = get_user_model()

        user_model.objects.create(
            username="user",
        )
        user_model.objects.create(
            username="staff",
            email="staff.user@example.com",
            is_staff=True,
        )
        john = user_model.objects.create(
            username="john",
            email="john.smith@example.com",
            first_name="John",
            last_name="Smith",
            is_staff=True,
        )
        john.is_active = False
        john.save()

        out = StringIO()
        call_command("list_staff_users", stdout=out, stderr=out)
        self.assertEqual(
            out.getvalue(),
            "\n".join(
                [
                    "-John Smith",  # Prefers get_full_name
                    "+staff.user",  # Uses email field, removes domain part.
                    "",  # blank line
                ]
            ),
        )
