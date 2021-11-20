from django.urls import path

from comments.views import (
    PostCommentsAPIView,
    WomanLeaveComment,
    LikeCommentOnlyDetailAPIView,
)

from .views import (
    AuthorDetailAPIView,
    AuthorListAPIView,
    CategorySpecialViews,
    CategoryViews,
    PostListAPIViews,
    UserLikesListAPIView,
    WomanCreateAPIView,
    WomanEditAPIView,
    WomanEditLikeUpdateView,
    WomanPutLikeCreateView,
    WomanPutLikeDetailListView,
    WomanPutLikeListView,
    WomanSpecialViews,
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
]
