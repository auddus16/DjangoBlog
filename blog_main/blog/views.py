from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag


# def index(request):
#
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts' : posts,
#         }
#     )
#
#
# def single_post_page(request, pk):
#
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post' : post,
#         }
#     )

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()

        return context


def show_category_posts(request, slug):
    if slug == 'no-category': # 미분류 글 요청
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug) # slug 값이 일치하는 카테고리
        post_list = Post.objects.filter(category=category)

    context = {
        'categories' : Category.objects.all(),
        'count_posts_without_category' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list # 위에서 만든 카테고리와 일치하는 게시글 리스트
    }

    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all() # tag가 나(tag)를 참조하고 있는 post를 전부 가져와라.

    context = {
        'categories': Category.objects.all(),
        'count_posts_without_category': Post.objects.filter(category=None).count(),
        'tag' : tag,
        'post_list' : post_list
    }
    return render(request, 'blog/post_list.html', context)