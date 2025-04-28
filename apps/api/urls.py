from django.urls import path, include
from .views import UploadFileView

urlpatterns = [
    path('auth/', include("apps.accounts.urls")),
    path('blog/', include("apps.blog.urls")),
    path("editorjs/upload", UploadFileView.as_view())
]