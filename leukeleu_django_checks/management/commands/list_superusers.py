from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

STATUS_FLAGS = {
    True: "+",
    False: "-",
}


def get_name(user: AbstractUser, email_field: str) -> str:
    name = user.get_full_name() or getattr(user, email_field) or user.get_username()
    return name.partition("@")[0]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        try:
            user_model = get_user_model()
        except ImproperlyConfigured:
            return

        if not hasattr(user_model, "is_superuser"):
            return

        superusers = user_model.objects.filter(is_superuser=True)
        email_field = user_model.get_email_field_name()

        name_status_list = sorted(
            ((get_name(user, email_field), user.is_active) for user in superusers),
            key=lambda item: item[0].casefold(),
        )
        for name, is_active in name_status_list:
            self.stdout.write(f"{STATUS_FLAGS[is_active]}{name}")
