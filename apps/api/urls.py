from django.urls import path, include
from .views import FileUploadAPIView, ContactAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "api"

urlpatterns = [
    path('auth/', include("apps.accounts.urls")),
    path('blog/', include("apps.blog.urls")),
    path("bot/", include("apps.chat.urls")),
    path("upload/", FileUploadAPIView.as_view()),
    path("contact/", ContactAPIView.as_view()),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(), name='docs'),
]