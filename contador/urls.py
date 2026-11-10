from django.urls import path

from .views import contador_async, contador_sync

urlpatterns = [
    path("sync/", contador_sync, name="contador_sync"),
    path("async/", contador_async, name="contador_async"),
]