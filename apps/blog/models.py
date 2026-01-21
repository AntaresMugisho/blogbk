from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models import F

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PostStatus(models.TextChoices):
    PUBLISHED = ('published', _('Published'))
    DRAFT = ('draft', _('Draft'))
    ARCHIVED = ('archived', _('Archived'))
    

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    content = models.JSONField()
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class PostInteractionType(models.TextChoices):
    LIKE = ('like', _('Like'))
    DISLIKE = ('dislike', _('Dislike'))


class UserPostInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_interactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_interactions')
    type = models.CharField(max_length=7, choices=PostInteractionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.post.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_interaction = None if is_new else UserPostInteraction.objects.get(pk=self.pk)
        
        # Update post like/dislike counts
        if is_new:
            if self.type == PostInteractionType.LIKE:
                self.post.likes = F('likes') + 1
            else:
                self.post.dislikes = F('dislikes') + 1
        else:
            # Switch from like to dislike or vice versa
            if old_interaction.type == PostInteractionType.LIKE:
                self.post.likes = F('likes') + 1
            else:
                self.post.dislikes = F('dislikes') + 1

        super().save(*args, **kwargs)
        self.post.save()

    def delete(self, *args, **kwargs):
        # Update post like/dislike counts on deletion
        if self.type == PostInteractionType.LIKE:
            self.post.likes = F('likes') - 1
        else:
            self.post.dislikes = F('dislikes') - 1
        self.post.save()
        super().delete(*args, **kwargs)
