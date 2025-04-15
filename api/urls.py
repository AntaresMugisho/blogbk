
from django.urls import path

urlpatterns = [
    path('auth/', include('accounts.urls')),
]