from django.urls import include

urlpatterns = [
    path('auth/', include("accounts.urls")),
    path('blog/', include("blog.urls")),
]