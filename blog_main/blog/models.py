import os.path

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# Tag 태그 모델
from markdown import markdown
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # URL에 들어갈 수 있는 문자열 필드

    # method
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


# Category 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # URL에 들어갈 수 있는 문자열 필드

    # method
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # 복수형 내가 정하고 싶을 때 (inner class)
    class Meta:
        verbose_name_plural = 'Categories'


# Post 게시글 모델
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook = models.CharField(max_length=50, default="이 글은 소개소개")
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지가 없어도 괜찮다. blank 속성 값 지정
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    def __str__(self):
        return f'[{self.pk}]  [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):    # 파일명이 경로가 아닌 이름으로 나오게 끔, 백에서
        return os.path.basename(self.attached_file.name)

    def get_markdown_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'