from django.urls import path, include
from .views import FileUploadAPIView

urlpatterns = [
    path('auth/', include("apps.accounts.urls")),
    path('blog/', include("apps.blog.urls")),
    path("bot/", include("apps.chat.urls")),
    path("upload/", FileUploadAPIView.as_view()),
]