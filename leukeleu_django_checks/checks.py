from django.conf import settings
from django.core import checks
from django.urls import Resolver404, resolve


class Tags:
    confidentiality = "confidentiality"
    email = "email"
    wagtail = "wagtail"
    files = "files"
    sentry = "sentry"
    urls = "urls"


W001 = checks.Warning(
    "You have not set the `FILE_UPLOAD_PERMISSIONS` setting to `0o644`.",
    id="leukeleu.W001",
)

W002 = checks.Warning(
    "You have set the `EMAIL_BACKEND` setting to"
    " `bandit.backends.smtp.HijackSMTPBackend`."
    " This is not recommended for production.",
    hint=(
        "Disable this warning in testing/staging by adding leukeleu.W002"
        " to SILENCED_SYSTEM_CHECKS."
    ),
    id="leukeleu.W002",
)

W003 = checks.Warning(
    "You have not set the `EMAIL_BACKEND` setting to"
    " `bandit.backends.smtp.HijackSMTPBackend`."
    " Using django-email-bandit is recommended for non-production environments.",
    hint=(
        "Disable this warning in production by adding leukeleu.W003"
        " to SILENCED_SYSTEM_CHECKS."
    ),
    id="leukeleu.W003",
)

W004 = checks.Warning(
    "You have not set the `WAGTAIL_ENABLE_UPDATE_CHECK` setting to `False`."
    " Besides checking for updates, this also provides the Wagtail team with"
    " the hostname of the project. Therefore it needs to be disabled.",
    id="leukeleu.W004",
)

W005 = checks.Warning(
    "The sentry-sdk package is not installed. You must install and configure"
    " sentry-sdk in order for application errors to be sent to Sentry.",
    id="leukeleu.W005",
)

W006 = checks.Warning(
    "The sentry-sdk package is installed but you have not configured a DSN."
    " This is required in order for application errors to be sent to Sentry.",
    id="leukeleu.W006",
)

W007 = checks.Warning(
    "Your URL patterns contain a /admin/ URL. This is not recommended.",
    id="leukeleu.W007",
)

I008 = checks.Info(
    "Your project does not have the leukeleu-django-gdpr package installed.",
    hint=(
        "Install the leukeleu-django-gdpr package and add"
        " 'leukeleu_django_gdpr' to INSTALLED_APPS."
    ),
    id="leukeleu.I008",
)

W009 = checks.Warning(
    "Your project is sending out emails but is not using SparkPost."
    " Please configure EMAIL_HOST to use SparkPost.",
    id="leukeleu.W009",
)


@checks.register(Tags.files)
def check_file_upload_permissions(app_configs, **kwargs):
    """
    Make sure FILE_UPLOAD_PERMISSIONS is set to 0o644 (the default since Django 3.2)
    """
    default_permissions = 0o644
    if getattr(settings, "FILE_UPLOAD_PERMISSIONS", None) != default_permissions:
        return [W001]
    else:
        return []


@checks.register(Tags.email, deploy=True)
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


@checks.register(Tags.wagtail, deploy=True)
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


@checks.register(Tags.sentry, deploy=True)
def check_sentry_dsn(app_configs, **kwargs):
    """
    Make sure sentry-sdk is installed and configured correctly
    """
    try:
        import sentry_sdk  # noqa: PLC0415
    except ImportError:
        return [W005]
    if sentry_sdk.Hub.current.client is None or not bool(
        sentry_sdk.Hub.current.client.dsn
    ):
        return [W006]
    else:
        return []


@checks.register(Tags.urls, deploy=True)
def check_admin_url(app_configs, **kwargs):
    """
    Make sure /admin or /admin/ is not used in URL patterns
    """
    for path in ["/admin", "/admin/"]:
        try:
            match = resolve(path)
        except Resolver404:  # noqa: PERF203
            continue
        else:
            if match.route.strip("/") == "admin":
                return [W007]
    return []


@checks.register(Tags.confidentiality)
def check_gdpr(app_configs, **kwargs):
    """
    Make sure leukeleu-django-gdpr is installed and configured correctly
    """
    if "leukeleu_django_gdpr" not in settings.INSTALLED_APPS:
        return [I008]
    else:
        return []


@checks.register(Tags.email, deploy=True)
def check_email_host(app_configs, **kwargs):
    """
    Make sure that projects that are sending out emails are using SparkPost.
    """
    if hasattr(settings, "EMAIL_HOST") and not settings.EMAIL_HOST.endswith(
        "sparkpostmail.com"
    ):
        return [W009]
    else:
        return []
