from django.apps import AppConfig


class LeukeleuDjangoChecksConfig(AppConfig):
    name = "leukeleu_django_checks"

    def ready(self):  # noqa: PLR6301
        # registers checks
        from . import checks  # noqa: F401, PLC0415
