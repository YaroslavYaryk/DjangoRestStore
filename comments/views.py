from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from store.models import WomanComment
from .serializers import (
    CommentPosListSerializer,
    CommentPostSerializer,
)
from store_api.pagination import PostPageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from store_api.views import BaseAPIView
from .serializers import (
    CommentAllSerializer,
    PostCommentCreateAPIView,
    CommentLikeCreateSerializer,
    CommentLikeViewSerializer,
    CommentLikeListSerializer,
)
from store.models import LikedComment

from rest_framework.mixins import (
    DestroyModelMixin,
    UpdateModelMixin,
    # RetrieveModelMixin,
    # CreateModelMixin,
)

# Create your views here.
class CommentPostListAPIView(BaseAPIView, ListAPIView):
    """A simple ViewSet that for listing or retrieving users."""

    queryset = WomanComment.objects.all()
    serializer_class = CommentPosListSerializer
    lookup_field = "slug"


class WomanLeaveComment(CreateAPIView):
    """leave comment"""

    queryset = WomanComment.objects.all()
    serializer_class = PostCommentCreateAPIView
    lookup_url_kwarg = "post_slug"
    permission_classes = [IsAuthenticatedOrReadOnly]


class WomanLeaveCommentUpdate(RetrieveUpdateAPIView):
    queryset = WomanComment.objects.all()
    serializer_class = CommentAllSerializer
    # lookup_field = "slug"


class WomanDeleteCommentView(RetrieveDestroyAPIView):
    queryset = WomanComment.objects.all()
    serializer_class = CommentPostSerializer
    # lookup_field = "comment_id"
    lookup_url_kwarg = "comment_id"


class PostCommentsAPIView(RetrieveAPIView):
    """all comments by a ppost"""

    queryset = WomanComment.objects.all()
    serializer_class = CommentAllSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeAPIView(BaseAPIView, ListCreateAPIView):
    """put like to comment"""

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeCreateSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class LikeCommentAPIView(BaseAPIView, ListAPIView):
    """put like to comment"""

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeViewSerializer


class LikeCommentOnlyDetailAPIView(RetrieveAPIView):
    """like detailed for like_comment/<pk>"""

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer


class LikeCommentDetailAPIView(RetrieveAPIView):
    """like detailed"""

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer
    lookup_url_kwarg = "like_id"


class LikeCommentEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """comment like edit"""

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer
    lookup_url_kwarg = "like_id"


class WomanEditCommentView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """edit comment"""

    queryset = WomanComment.objects.filter(id__gt=0)
    serializer_class = CommentPostSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
