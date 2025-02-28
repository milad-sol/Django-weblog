from django.contrib import admin
from .models import Post, Category, Comment


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'categories', 'slug', 'hot_post', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    search_fields = ('title',)


@admin.register(Comment)
class CommentInline(admin.ModelAdmin):
    list_display = ['post', 'post_id', 'author', 'is_reply', 'created_at', 'updated_at']

