from django.urls import path
from .views import repos_sync, repos_async

urlpatterns = [
    path("sync/", repos_sync, name="repos_sync"),
    path("async/", repos_async, name="repos_async"),
]