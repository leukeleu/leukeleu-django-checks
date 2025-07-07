# Leukeleu Django Checks

Additional deploy checks and other tools to validate if a Django project is set up correctly.

## Installation

Add `'leukeleu_django_checks'` to `INSTALLED_APPS`.

## Included checks

* `leukeleu.W001`: Check if `FILE_UPLOAD_PERMISSIONS` is set to `0o644`
* `leukeleu.W002`: Check if `EMAIL_BACKEND` is set to `bandit.backends.smtp.HijackSMTPBackend`
  * Disable this for test/staging environments using `SILENCED_SYSTEM_CHECKS`
* `leukeleu.W003`: Check if `EMAIL_BACKEND` is **not** set to `bandit.backends.smtp.HijackSMTPBackend`
  * Disable this for production environments using `SILENCED_SYSTEM_CHECKS`
* `leukeleu.W004`: Check if `WAGTAIL_ENABLE_UPDATE_CHECK` is set to `False`
  * This check only runs if wagtail is installed
* `leukeleu.W005`: Check if `sentry-sdk` is installed
* `leukeleu.W006`: Check if `sentry-sdk` is configured correctly
* `leukeleu.W007`: Make sure there is no `/admin` or `/admin/` url
* `leukeleu.I008`: Check if `leukeleu-django-gdpr` is in `INSTALLED_APPS`

Run `./manage.py check --deploy` to execute these checks (in addition to Django's default set).

## List superusers

Run `./manage.py list_superusers` to print a list of all (in)active superusers.

The name of each superuser is printed with a "+" (active) or "-" (inactive) prefix.

## List staff users

Run `./manage.py list_staff_users` to print a list of all (in)active staff users.

The name of each staff user is printed with a "+" (active) or "-" (inactive) prefix.
