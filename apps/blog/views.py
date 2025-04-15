from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.db.models import F
from .models import Post, Tag, Comment, UserPostInteraction
from .serializers import (
    PostSerializer, TagSerializer, CommentSerializer,
    UserPostInteractionSerializer
)

# Create your views here.

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(deleted_at__isnull=True)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

class UserPostInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = UserPostInteractionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return UserPostInteraction.objects.filter(user=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'views', 'likes', 'dislikes']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        else:
            # By default, show only published posts
            queryset = queryset.filter(status=Post.PostStatus.PUBLISHED)
        
        # Filter by deleted status
        deleted = self.request.query_params.get('deleted')
        if deleted is not None:
            if deleted.lower() == 'true':
                queryset = queryset.filter(deleted_at__isnull=False)
            else:
                queryset = queryset.filter(deleted_at__isnull=True)
        else:
            # By default, exclude deleted posts
            queryset = queryset.filter(deleted_at__isnull=True)
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views (May be this will be moved later. Why ? Cause we only want to increment post views when 
        # some bottom element on the post detail page is intercepted in the browser viewport)
        instance.views = F('views') + 1
        instance.save()
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        post = self.get_object()
        interaction, created = UserPostInteraction.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'interaction_type': UserPostInteraction.InteractionType.LIKE}
        )
        
        if not created:
            if interaction.interaction_type == UserPostInteraction.InteractionType.LIKE:
                interaction.delete()
                return Response({'status': 'like removed'})
            else:
                interaction.interaction_type = UserPostInteraction.InteractionType.LIKE
                interaction.save()
        
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def dislike(self, request, slug=None):
        post = self.get_object()
        interaction, created = UserPostInteraction.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'interaction_type': UserPostInteraction.InteractionType.DISLIKE}
        )
        
        if not created:
            if interaction.interaction_type == UserPostInteraction.InteractionType.DISLIKE:
                interaction.delete()
                return Response({'status': 'dislike removed'})
            else:
                interaction.interaction_type = UserPostInteraction.InteractionType.DISLIKE
                interaction.save()
        
        return Response({'status': 'disliked'})
