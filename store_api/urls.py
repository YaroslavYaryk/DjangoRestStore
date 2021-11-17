from django.urls import path
from .views import (AuthorDetailAPIView, AuthorListAPIView, CategorySpecialViews, 
    CategoryViews, CommentLikeAPIView, CommentPostListAPIView,
    LikeCommentAPIView, LikeCommentDetailAPIView, PostCommentsAPIView, PostListAPIViews, UserLikesListAPIView, 
    WomanCreateAPIView, WomanDeleteAPIView, 
    WomanDeleteCommentView, WomanLeaveComment, WomanLeaveCommentUpdate, WomanPutLikeCreateView, WomanPutLikeListView, 
    WomanPutLikeUpdateView, WomanSpecialViews, WomanUpdateAPIView)


urlpatterns = [
    path("posts/", PostListAPIViews.as_view(), name="post-list"),
    path("posts/<slug:post_slug>/", WomanSpecialViews.as_view(), name="list-special-post"),
    path("category/", CategoryViews.as_view(), name="list-category"),
    path("category/<int:cat_id>", CategorySpecialViews.as_view(), name="list-category-special"),
    path("create_post/", WomanCreateAPIView.as_view(), name="create-view"),
    path('posts/<slug>/update', WomanUpdateAPIView.as_view(), name="update-view"),
    path("posts/<slug>/delete", WomanDeleteAPIView.as_view(), name="delete-view"),
    path("posts/<slug:post_slug>/comments/", PostCommentsAPIView.as_view(), name='post-comments'),
    path("leave_comment/", WomanLeaveComment.as_view(), name='leave-comment'),
    path("leave_comment/<pk>/update", WomanLeaveCommentUpdate.as_view(), name='comment-update'),
    path("comment/<int:comment_id>/delete", WomanDeleteCommentView.as_view(), name="delete-comment"),
    path("comments/", CommentPostListAPIView.as_view(), name="comment"),
    path("comments/<int:comment_id>/", PostCommentsAPIView.as_view(), name="comment-details"),
    path("create_like/", WomanPutLikeCreateView.as_view(), name="create-like"),
    path("post_likes/", WomanPutLikeListView.as_view(), name="posts-likes"),
    path("post_likes/<pk>", WomanPutLikeListView.as_view(), name="detail-likes"),
    path("user_likes/", UserLikesListAPIView.as_view(), name="user-comment-likes"),
    path("like_update/<pk>", WomanPutLikeUpdateView.as_view(), name='like-update'),
    path("comments/<pk>/add_like/", CommentLikeAPIView.as_view(), name="like-comment"),
    path("comments/<pk>/likes/", LikeCommentAPIView.as_view(), name="comment-likes"),
    path("comments/<pk>/likes/<int:like_id>", LikeCommentDetailAPIView.as_view(), name="detail-like"),
    path("authors/", AuthorListAPIView.as_view(), name="authors-list"),
    path("authors/<int:author_id>/", AuthorDetailAPIView.as_view(), name="authors-detail"),

]


