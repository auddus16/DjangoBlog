import os.path

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지가 없어도 괜찮다. blank 속성 값 지정
    attached_file = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    def __str__(self):
        return f'[{self.pk}]  [{self.title}]'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):    # 파일명이 경로가 아닌 이름으로 나오게끔, 백에서
        return os.path.basename(self.attached_file.name)