from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    # path('<int:pk>/', views.single_post_page),  # <자료형:변수명> -> single_post_page의 매개변수로 넘어간다.
    path('<int:pk>/', views.PostDetail.as_view()),  # <자료형:변수명> -> single_post_page의 매개변수로 넘어간다.
    # path('', views.index)
    path('<int:pk>/add_comment/', views.add_comment),

    path('category/<str:slug>/', views.show_category_posts),
    path('tag/<str:slug>/', views.show_tag_posts),

    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/',views.PostUpdate.as_view() )
]