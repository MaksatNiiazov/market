from django.urls import path
from tanda_backend.products.views import upload_file_api

urlpatterns = [
    path("file/", upload_file_api),
]
