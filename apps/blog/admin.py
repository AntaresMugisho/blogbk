from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'status', 'updated_at')
    list_filter = ('author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

