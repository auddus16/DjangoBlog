from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Post, Category, Tag, Comment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )} # slug 필드에서는 name 값을 그대로 넣어주세요. 뒤에 튜플 형태로 넣은 거 유의

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

# Register your models here.
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)