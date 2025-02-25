from django.db import models
from django.utils.text import slugify

from accounts.models import User
from django.shortcuts import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # TODO:set if slug have space automatically remove it
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})


# Create your models here.
class Post(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='static/images/posts/')
    hot_post = models.BooleanField(default=False, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    keywords = models.CharField(null=True, blank=True, verbose_name='separated with comma (,)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})
