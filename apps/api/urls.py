from django.urls import path, include

urlpatterns = [
    path('auth/', include("apps.accounts.urls")),
    path('blog/', include("apps.blog.urls")),
]