from django.apps import AppConfig


class LeukeleuDjangoChecksConfig(AppConfig):
    name = "leukeleu_django_checks"

    def ready(self):
        # registers checks
        from . import checks  # noqa: F401
