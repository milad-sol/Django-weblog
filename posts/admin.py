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
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'is_reply', 'parent', 'created_at')
    list_filter = ('is_reply', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)

    raw_id_fields = ('author', 'post', 'parent')




