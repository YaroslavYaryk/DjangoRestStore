# from rest_framework import pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

# from rest_framework.views import APIView
from store_api.pagination import PostPageNumberPagination
from store.models import Author, LikedComment, Woman, Category, WomanLike
from comments.serializers import CommentLikeListSerializer
from .serializers import (
    AuthoeSerializer,
    PostLikeCreateSerializer,
    PostLikeListSerializer,
    PostLikeUpdateSerializer,
    WomanCreateSerializer,
    WomanSerializer,
    CatSerializer,
    WomanSpecialUpdateSerializer,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .pormissions import IsOwnerOrReadOnly
from rest_framework.mixins import (
    DestroyModelMixin,
    UpdateModelMixin,
    # RetrieveModelMixin,
    # CreateModelMixin,
)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """

    queryset = Category.objects.all()

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CatSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CatSerializer(user)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving authors.
    """

    queryset = Author.objects.all()

    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthoeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        print()
        queryset = Author.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AuthoeSerializer(user)
        return Response(serializer.data)


class BaseAPIView:
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    order_fields = ["title", "content"]


# class CategoryPostListAPIView(BaseAPIView, ListAPIView):
#     """A simple ViewSet that for listing or retrieving users."""

#     queryset = Category.objects.all()
#     serializer_class = CatSerializer
#     pagination_class = PostPageNumberPagination


class PostListAPIViews(BaseAPIView, ListAPIView):
    """get all posts"""

    queryset = Woman.objects.filter(is_published=True)
    serializer_class = WomanSerializer
    pagination_class = PostPageNumberPagination


# class CategoryViews(BaseAPIView, ListAPIView):
#     """get all categories"""

#     queryset = Category.objects.all()
#     serializer_class = CatSerializer


# class CategorySpecialViews(APIView):
#     """get special category by cat id"""

#     def get(self, request, cat_id):

#         catrgory = Category.objects.get(pk=cat_id)
#         serializer = CatSerializer(catrgory)
#         return Response(serializer.data)


class WomanSpecialViews(RetrieveDestroyAPIView):
    """get special category by cat id"""

    queryset = Woman.objects.all()
    serializer_class = WomanSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "post_slug"
    permission_classes = [IsOwnerOrReadOnly]

    # def get(self, request, post_id):

    #     post = Woman.objects.get(pk = post_id)
    #     serializer = WomanSpecialSerializer(post)
    #     return Response(serializer.data)


class WomanEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanSpecialUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WomanDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanSpecialUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser]


class WomanCreateAPIView(ListCreateAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanCreateSerializer
    permission_classes = [IsAuthenticated]


class WomanPutLikeCreateView(CreateAPIView):
    """create like to post"""

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeCreateSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserLikesListAPIView(BaseAPIView, ListAPIView):
    """all user likes"""

    # queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):

        return LikedComment.objects.filter(user=self.request.user)


class WomanEditLikeUpdateView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """update post like"""

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeUpdateSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WomanPutLikeListView(ListAPIView):
    """how all post like"""

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeListSerializer
    pagination_class = PostPageNumberPagination


# class WomanPutLikeListView(ListAPIView):
#     """how all post like"""

#     queryset = WomanLike.objects.all()
#     serializer_class = PostLikeListSerializer


class WomanPutLikeDetailListView(RetrieveAPIView):
    """how all post like"""

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeListSerializer


# class AuthorListAPIView(ListAPIView):
#     """all authors"""

#     queryset = Author.objects.all()
#     serializer_class = AuthoeSerializer
#     pagination_class = pagination.LimitOffsetPagination


# class AuthorDetailAPIView(RetrieveAPIView):
#     """detail authors"""

#     queryset = Author.objects.all()
#     serializer_class = AuthoeSerializer
#     lookup_url_kwarg = "author_id"
