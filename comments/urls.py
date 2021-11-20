from django.urls import path
from .views import (
    CommentPostListAPIView,
    LikeCommentDetailAPIView,
    PostCommentsAPIView,
    WomanEditCommentView,
    CommentLikeAPIView, LikeCommentAPIView
)

urlpatterns = [
    path(
        "<int:comment_id>/edit/",
        WomanEditCommentView.as_view(),
        name="edit-comment",
    ),
    path("", CommentPostListAPIView.as_view(), name="comment"),
    path(
        "<pk>/",
        PostCommentsAPIView.as_view(),
        name="comment-details",
    ),
    path("<pk>/likes/", LikeCommentAPIView.as_view(), name="comment-likes"),
    path(
        "<pk>/likes/<int:like_id>/",
        LikeCommentDetailAPIView.as_view(),
        name="detail-like",
    ),
    path("<pk>/add_like/", CommentLikeAPIView.as_view(), name="like-comment"),
]
