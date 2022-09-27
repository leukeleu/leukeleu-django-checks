from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    # pragma: no cover
    path("admin/", lambda request: HttpResponse("Hello admin!"))
]
