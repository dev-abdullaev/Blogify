from django.urls import path

from .views import (CategoryCreateView, CategoryView, CommentCreateView,
                    CommentDeleteView, CommentUpdateView, LikeView,
                    PostCreateView, PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView, SearchResultsListView,
                    reply_comment)

urlpatterns = [
    path("home/", PostListView.as_view(), name="home"),
    path("category-add/", CategoryCreateView.as_view(), name="category_add"),
    path("category/<str:cats>/", CategoryView, name="category"),
    path("", PostListView.as_view(), name="post_list"),
    path("post-create/", PostCreateView.as_view(), name="post_create"),
    path("post-detail/<int:pk>/", PostDetailView, name="post_detail"),
    path("post-update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("post-delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("like/<int:pk>/", LikeView, name="like_post"),
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="add_comment"),
    path("post/<int:pk>/comment-update/", CommentUpdateView.as_view(), name="comment_update"),
    path("post/<int:pk>/comment-delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path("comment/reply/", reply_comment, name="reply"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
]
