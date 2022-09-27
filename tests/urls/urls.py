from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    # pragma: no cover
    path("not-admin/", lambda request: HttpResponse("Hello regular user!"))
]
