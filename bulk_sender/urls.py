from django.urls import path
from .views import upload_file, success_page

urlpatterns = [
    path("", upload_file, name="upload_file"),
    path("success/", success_page, name="success_page")
]
