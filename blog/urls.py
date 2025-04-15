from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, 
    CommentViewSet, 
    UserPostInteractionViewSet, 
    PostViewSet
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'interactions', UserPostInteractionViewSet, basename='interaction')

urlpatterns = [
    path("", include(router.urls))
]