from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    # path('<int:pk>/', views.single_post_page),  # <자료형:변수명> -> single_post_page의 매개변수로 넘어간다.
    path('<int:pk>/', views.PostDetail.as_view()),  # <자료형:변수명> -> single_post_page의 매개변수로 넘어간다.
    # path('', views.index)
]