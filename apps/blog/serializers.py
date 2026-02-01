from rest_framework import serializers
from .models import Post, Tag, Comment, Category, UserPostInteraction

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug']

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at', 'posts_count']
        read_only_fields = ['slug']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class UserPostInteractionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = UserPostInteraction
        fields = ['id', 'user', 'user_username', 'post', 'post_title', 
                 'type', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_interaction = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'status', 'status_display',
            'likes', 'dislikes', 'views', 'category', 'category_id',
            'author', 'author_username', 'tags', 'comments',
            'comment_count', 'created_at', 'updated_at', 'deleted_at',
            'user_interaction'
        ]
        read_only_fields = ['slug', 'author', 'likes', 'dislikes', 'views']

    def get_user_interaction(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                interaction = obj.user_interactions.get(user=request.user)
                return interaction.type
            except UserPostInteraction.DoesNotExist:
                return None
        return None

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user
        post = super().create(validated_data)
        
        # Handle tags
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = super().update(instance, validated_data)
        
        if tags_data:
            post.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                post.tags.add(tag)
        
        return post
