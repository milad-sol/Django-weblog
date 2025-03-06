from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from accounts.models import User
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class BaseTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Seo(models.Model):
    page_title = models.CharField(max_length=70, help_text='Recommended 50-70 characters ')
    slug = models.SlugField(unique=True, max_length=200, help_text='Recommended 50-70 characters ')
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        help_text="Recommended: 150-160 characters for meta description"
    )

    class Meta:
        verbose_name = "SEO Metadata"
        verbose_name_plural = "SEO Metadata Entries"
        abstract = True

    def clean(self):

        if not self.slug:
            self.slug = slugify(self.page_title)
        if self.meta_description and len(self.meta_description) > 160:
            raise ValidationError('Meta description must be 160 characters or less.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Seo, self).save(*args, **kwargs)


class Category(BaseTimeStamp, Seo):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextField(max_length=200)

    # TODO:add a summery about category
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
        return reverse('posts:single_category', kwargs={'slug': self.slug})


# Create your models here.
class Post(BaseTimeStamp, Seo):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='featured-images/')
    breaking_news = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    keywords = models.CharField(null=True, blank=True, verbose_name='separated with comma (,)')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})


class Comment(BaseTimeStamp):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_reply = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return '{} - {}'.format(self.author, self.content[:30])
