from django.http import HttpResponse
from django.urls import path, re_path

urlpatterns = [
    # pragma: no cover
    path("not-admin/", lambda request: HttpResponse("Hello regular user!")),
    re_path(r"(?P<name>\w+)/", lambda request, name: HttpResponse(f"Hello {name}!")),
]
