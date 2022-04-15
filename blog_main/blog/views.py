from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'hook', 'head_image', 'attached_file', 'category']

    template_name = "blog/post_form_update.html"

    def dispatch(self, request, *args, **kwarngs): # get에서도 user 권한을 분석하겠다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwarngs)
        else:
            raise PermissionDenied

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): # LoginRequiredMinin : 로그인을 한 상태에서만 글을 쓸 수 있게
    model = Post
    fields = ['title', 'content', 'hook', 'head_image', 'attached_file', 'category']

    def test_func(self): # 들어온 사용자의 등급을 확인하는 메소드
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user # request에서 user를 받아서 저장

        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            # 로그인 되었을 뿐 아니라, 로그인 된 사용자의 등급을 확인
            form.instance.author = current_user # form의 instance의 author 자리에 지금 사용자를 넣어서

            return super(PostCreate, self).form_valid(form) # author가 추가된 form상태로 집어넣는다.
        else:
            return redirect('/blog/')

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


