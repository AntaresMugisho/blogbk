from django.urls import path
from .views import ChatBotView

urlpatterns = [
    path('c/<str:session_id>/', ChatBotView.as_view(), name='chatbot'),
]
