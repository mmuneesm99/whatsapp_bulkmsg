from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("", include("bulk_sender.urls")),
    path('admin/', admin.site.urls),
]
