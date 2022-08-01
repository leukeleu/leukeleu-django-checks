from django.conf import settings
from django.core.checks import Warning, register


class Tags:
    email = "email"
    wagtail = "wagtail"
    files = "files"
    sentry = "sentry"


W001 = Warning(
    "You have not set the `FILE_UPLOAD_PERMISSIONS` setting to `0o644`.",
    id="leukeleu.W001",
)

W002 = Warning(
    "You have set the `EMAIL_BACKEND` setting to"
    " `bandit.backends.smtp.HijackSMTPBackend`."
    " This is not recommended for production.",
    hint=(
        "Disable this warning in testing/staging by adding leukeleu.W002"
        " to SILENCED_SYSTEM_CHECKS."
    ),
    id="leukeleu.W002",
)

W003 = Warning(
    "You have not set the `EMAIL_BACKEND` setting to"
    " `bandit.backends.smtp.HijackSMTPBackend`."
    " Using django-email-bandit is recommended for non-production environments.",
    hint=(
        "Disable this warning in production by adding leukeleu.W003"
        " to SILENCED_SYSTEM_CHECKS."
    ),
    id="leukeleu.W003",
)

W004 = Warning(
    "You have not set the `WAGTAIL_ENABLE_UPDATE_CHECK` setting to `False`."
    " Besides checking for updates, this also provides the Wagtail team with"
    " the hostname of the project. Therefore it needs to be disabled.",
    id="leukeleu.W004",
)

W005 = Warning(
    "The sentry-sdk package is not installed. You must install and configure"
    " sentry-sdk in order for application errors to be sent to Sentry.",
    id="leukeleu.W005",
)

W006 = Warning(
    "The sentry-sdk package is installed but you have not configured a DSN."
    " This is required in order for application errors to be sent to Sentry.",
    id="leukeleu.W006",
)


@register(Tags.files)
def check_file_upload_permissions(app_configs, **kwargs):
    """
    Make sure FILE_UPLOAD_PERMISSIONS is set to 0o644 (the default since Django 3.2)
    """
    if getattr(settings, "FILE_UPLOAD_PERMISSIONS", None) != 0o644:
        return [W001]
    else:
        return []


@register(Tags.email, deploy=True)
def check_email_backend(app_configs, **kwargs):
    """
    Make sure EMAIL_BACKEND is (not) set to bandit.backends.smtp.HijackSMTPBackend
    """
    # This will always return a warning as using email-bandit is bad in production
    # and **not** using it is bad in staging and test environments.
    if (
        getattr(settings, "EMAIL_BACKEND", None)
        == "bandit.backends.smtp.HijackSMTPBackend"
    ):
        return [W002]
    else:
        return [W003]


@register(Tags.wagtail, deploy=True)
def check_wagtail_update_check(app_configs, **kwargs):
    """
    Make sure WAGTAIL_ENABLE_UPDATE_CHECK is set to False when wagtail is installed
    """
    if (
        "wagtail" in settings.INSTALLED_APPS  # Wagtail 3.x
        or "wagtail.core" in settings.INSTALLED_APPS  # Wagtail 2.x
    ) and getattr(settings, "WAGTAIL_ENABLE_UPDATE_CHECK", True) is True:
        return [W004]
    else:
        return []


@register(Tags.sentry, deploy=True)
def check_sentry_dsn(app_configs, **kwargs):
    """
    Make sure sentry-sdk is installed and configured correctly
    """
    try:
        import sentry_sdk
    except ImportError:
        return [W005]
    if sentry_sdk.Hub.current.client is None or not bool(
        sentry_sdk.Hub.current.client.dsn
    ):
        return [W006]
    else:
        return []
