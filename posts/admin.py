from django.contrib import admin
from .models import Post, Category, Comment, Seo


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'categories', 'slug', 'is_published', 'breaking_news', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    fieldsets = [
        ('Main', {'fields': ['title', 'slug', 'content', 'featured_image', 'breaking_news', 'is_published', 'author',
                             'categories']}),
        ('Seo', {'fields': ['page_title', 'meta_description']})
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

    fieldsets = [
        ('Main', {'fields': ['title', 'slug', 'description', ]}),
        ('Seo', {'fields': ['page_title', 'meta_description']})
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_reply', 'created_at')
    list_filter = ('is_reply', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)

    raw_id_fields = ('author', 'post', 'parent')
