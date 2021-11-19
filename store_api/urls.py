from django.urls import path
from .views import (
    AuthorDetailAPIView,
    AuthorListAPIView,
    CategorySpecialViews,
    CategoryViews,
    CommentLikeAPIView,
    CommentPostListAPIView,
    LikeCommentAPIView,
    LikeCommentDetailAPIView,
    PostCommentsAPIView,
    PostListAPIViews,
    UserLikesListAPIView,
    WomanCreateAPIView,
    WomanEditAPIView,
    WomanEditCommentView,
    WomanEditLikeUpdateView,
    WomanLeaveComment,
    WomanPutLikeCreateView,
    WomanPutLikeDetailListView,
    WomanPutLikeListView,
    WomanSpecialViews,
    LikeCommentOnlyDetailAPIView,
    UserCreateView,
)


urlpatterns = [
    path("posts/", PostListAPIViews.as_view(), name="post-list"),
    path(
        "posts/<slug:post_slug>/", WomanSpecialViews.as_view(), name="list-special-post"
    ),
    path(
        "posts/<slug:post_slug>/leave_comment/",
        WomanLeaveComment.as_view(),
        name="leave-comment",
    ),
    path(
        "posts/<slug:post_slug>/create_like/",
        WomanPutLikeCreateView.as_view(),
        name="create-like",
    ),
    path("posts/<slug>/edit/", WomanEditAPIView.as_view(), name="update-view"),
    path(
        "posts/<slug:post_slug>/comments/",
        PostCommentsAPIView.as_view(),
        name="post-comments",
    ),
    path("category/", CategoryViews.as_view(), name="list-category"),
    path(
        "category/<int:cat_id>",
        CategorySpecialViews.as_view(),
        name="list-category-special",
    ),
    path("create_post/", WomanCreateAPIView.as_view(), name="create-view"),
    path(
        "comments/<int:comment_id>/edit/",
        WomanEditCommentView.as_view(),
        name="edit-comment",
    ),
    path("comments/", CommentPostListAPIView.as_view(), name="comment"),
    path(
        "comments/<pk>/",
        PostCommentsAPIView.as_view(),name="comment-details",
    ),
    path("comments/<pk>/likes/", LikeCommentAPIView.as_view(), name="comment-likes"),
    path(
        "comments/<pk>/likes/<int:like_id>/",
        LikeCommentDetailAPIView.as_view(),
        name="detail-like",
    ),
    path("comments/<pk>/add_like/", CommentLikeAPIView.as_view(), name="like-comment"),
    path("post_likes/", WomanPutLikeListView.as_view(), name="posts-likes"),
    path("post_likes/<pk>/", WomanPutLikeDetailListView.as_view(), name="detail-likes"),
    path(
        "likes_comment/<pk>/",
        LikeCommentOnlyDetailAPIView.as_view(),
        name="detail-comment-likes",
    ),
    path("post_likes/<pk>/edit/", WomanEditLikeUpdateView.as_view(), name="edit-likes"),
    path("user_likes/", UserLikesListAPIView.as_view(), name="user-comment-likes"),
    path("authors/", AuthorListAPIView.as_view(), name="authors-list"),
    path(
        "authors/<int:author_id>/", AuthorDetailAPIView.as_view(), name="authors-detail"
    ),
    path("register/", UserCreateView.as_view(), name="user_register"),
]
