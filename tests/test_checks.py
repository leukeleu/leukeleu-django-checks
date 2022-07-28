import importlib

from unittest import mock

from django.test import SimpleTestCase, modify_settings, override_settings

from leukeleu_django_checks import checks


class TestCheckFileUploadPermissions(SimpleTestCase):
    @override_settings(FILE_UPLOAD_PERMISSIONS=0o666)
    def test_bad_permissions(self):
        self.assertEqual([checks.W001], checks.check_file_upload_permissions(None))

    @override_settings(FILE_UPLOAD_PERMISSIONS=0o644)
    def test_correct_permissions(self):
        self.assertEqual([], checks.check_file_upload_permissions(None))


class TestCheckEmailBackend(SimpleTestCase):
    @override_settings(EMAIL_BACKEND="bandit.backends.smtp.HijackSMTPBackend")
    def test_hijack_email_backend(self):
        self.assertEqual([checks.W002], checks.check_email_backend(None))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
    def test_smtp_email_backend(self):
        self.assertEqual([checks.W003], checks.check_email_backend(None))


class TestCheckWagtailUpdateCheck(SimpleTestCase):
    def setUp(self):
        # Temporarily add wagtail to sys.modules, but point it to the
        # fake tests.mocks.mock_wagtail module, this allows us to
        # put wagtail (and wagtail.core) into INSTALLED_APPS without
        # Django's apps registry exploding.
        patch_sys_modules = mock.patch.dict(
            "sys.modules",
            {
                "wagtail": importlib.import_module("tests.mocks.mock_wagtail"),
            },
        )
        patch_sys_modules.start()
        self.addCleanup(patch_sys_modules.stop)

    @modify_settings(INSTALLED_APPS={"append": "wagtail"})
    def test_wagtail_3_update_check_unset(self):
        self.assertEqual([checks.W004], checks.check_wagtail_update_check(None))

    @modify_settings(INSTALLED_APPS={"append": "wagtail"})
    @override_settings(WAGTAIL_ENABLE_UPDATE_CHECK=True)
    def test_wagtail_3_update_check_enabled(self):
        self.assertEqual([checks.W004], checks.check_wagtail_update_check(None))

    @modify_settings(INSTALLED_APPS={"append": "wagtail"})
    @override_settings(WAGTAIL_ENABLE_UPDATE_CHECK=False)
    def test_wagtail_3_update_check_disabled(self):
        self.assertEqual([], checks.check_wagtail_update_check(None))

    @modify_settings(INSTALLED_APPS={"append": "wagtail.core"})
    def test_wagtail_2_update_check_unset(self):
        self.assertEqual([checks.W004], checks.check_wagtail_update_check(None))

    @modify_settings(INSTALLED_APPS={"append": "wagtail.core"})
    @override_settings(WAGTAIL_ENABLE_UPDATE_CHECK=True)
    def test_wagtail_2_update_check_enabled(self):
        self.assertEqual([checks.W004], checks.check_wagtail_update_check(None))

    @modify_settings(INSTALLED_APPS={"append": "wagtail.core"})
    @override_settings(WAGTAIL_ENABLE_UPDATE_CHECK=False)
    def test_wagtail_2_update_check_disabled(self):
        self.assertEqual([], checks.check_wagtail_update_check(None))

    def test_wagtail_not_in_installed_apps(self):
        self.assertEqual([], checks.check_wagtail_update_check(None))


class TestCheckSentryDSN(SimpleTestCase):
    def setUp(self):
        self.mock_sentry_sdk = importlib.import_module("tests.mocks.mock_sentry_sdk")
        self.patch_sys_modules = mock.patch.dict(
            "sys.modules",
            {"sentry_sdk": self.mock_sentry_sdk},
        )
        self.patch_sys_modules.start()
        self.addCleanup(self.patch_sys_modules.stop)

    def test_sentry_sdk_not_installed(self):
        self.patch_sys_modules.stop()  # Stop faking the installation of sentry-sdk
        self.assertEqual([checks.W005], checks.check_sentry_dsn(None))

    def test_sentry_sdk_installed_no_client(self):
        self.assertEqual([checks.W006], checks.check_sentry_dsn(None))

    def test_sentry_sdk_installed_with_client_no_dsn(self):
        with mock.patch(
            "sentry_sdk.Hub.current",
            new_callable=mock.PropertyMock,
            return_value=self.mock_sentry_sdk.Hub(self.mock_sentry_sdk.Client()),
        ):
            self.assertEqual([checks.W006], checks.check_sentry_dsn(None))

    def test_sentry_sdk_installed_and_configured(self):
        with mock.patch(
            "sentry_sdk.Hub.current",
            new_callable=mock.PropertyMock,
            return_value=self.mock_sentry_sdk.Hub(
                self.mock_sentry_sdk.Client(dsn="https://public@sentry.example.com/1")
            ),
        ):
            self.assertEqual([], checks.check_sentry_dsn(None))
