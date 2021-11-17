from django.db.models import query
from rest_framework import pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
    RetrieveDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from store_api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from store.models import Author, LikedComment, Woman, Category, WomanComment, WomanLike
from .serializers import (
    AuthoeSerializer, CommentAllSerializer, CommentLikeCreateSerializer, CommentLikeListSerializer, 
    CommentLikeViewSerializer, CommentPosListSerializer, 
    CommentPostSerializer, PostCommentCreateAPIView, PostLikeCreateSerializer, PostLikeListSerializer, 
    WomanCreateSerializer, WomanSerializer, CatSerializer, WomanSpecialSerializer,
     WomanSpecialUpdateSerializer)
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser,
    IsAuthenticatedOrReadOnly)



class BaseAPIView():
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    order_fields = ["title", "content"]


class CategoryPostListAPIView(BaseAPIView, ListAPIView):
    """ A simple ViewSet that for listing or retrieving users."""

    queryset = Category.objects.all()
    serializer_class = CatSerializer
    pagination_class = PostPageNumberPagination

class CommentPostListAPIView(BaseAPIView, ListAPIView):
    """ A simple ViewSet that for listing or retrieving users."""

    queryset = WomanComment.objects.all()
    serializer_class = CommentPosListSerializer
    lookup_field = "slug"


class PostListAPIViews(BaseAPIView, ListAPIView):
    """ get all posts """
    
    queryset = Woman.objects.filter(is_published=True)
    serializer_class = WomanSerializer
    pagination_class = PostPageNumberPagination

class CategoryViews(BaseAPIView, ListAPIView):
    """ get all categories """  

    queryset = Category.objects.all()
    serializer_class = CatSerializer

    

class CategorySpecialViews(APIView):
    """ get special category by cat id """

    def get(self, request, cat_id):

        catrgory = Category.objects.get(pk = cat_id)
        serializer = CatSerializer(catrgory)
        return Response(serializer.data)        


class WomanSpecialViews(RetrieveAPIView):
    """ get special category by cat id """

    queryset = Woman.objects.all()
    serializer_class = WomanSpecialSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "post_slug"

    # def get(self, request, post_id):

    #     post = Woman.objects.get(pk = post_id)
    #     serializer = WomanSpecialSerializer(post)
    #     return Response(serializer.data)                


class WomanUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanSpecialUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser]


class WomanDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanSpecialUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser]

class WomanCreateAPIView(ListCreateAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomanCreateSerializer
    # permission_classes = [IsAuthenticated]

class WomanLeaveComment(CreateAPIView):
    """ leave comment """

    queryset = WomanComment.objects.all()
    serializer_class = PostCommentCreateAPIView
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # def post(self, request):
    #     comment = CommentPostSerializer(data=request.data)   
    #     if comment.is_valid():
    #         comment.save()
    #         return Response(status=201)
    #     return Response(status=500)        


class WomanLeaveCommentUpdate(RetrieveUpdateAPIView):
    queryset = WomanComment.objects.all()
    serializer_class = CommentAllSerializer
    # lookup_field = "slug"


class WomanDeleteCommentView(RetrieveDestroyAPIView):
    queryset = WomanComment.objects.all()
    serializer_class = CommentPostSerializer
    # lookup_field = "comment_id"
    lookup_url_kwarg = "comment_id"


class PostCommentsAPIView(ListAPIView):
    """ all comments by a ppost """

    queryset = WomanComment.objects.all()
    serializer_class = CommentPostSerializer
    lookup_url_kwarg = "comment_id"

    
class WomanPutLikeCreateView(CreateAPIView):
    """ create like to post """

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeCreateSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserLikesListAPIView(BaseAPIView, ListAPIView):
    """ all user likes """

    # queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):

        return LikedComment.objects.filter(user = self.request.user) 

class WomanPutLikeUpdateView(RetrieveUpdateAPIView):
    """ update post like """

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeCreateSerializer
    pagination_class = PostPageNumberPagination


class WomanPutLikeListView(ListAPIView):
    """ how all post like """

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeListSerializer
    pagination_class = PostPageNumberPagination


class WomanPutLikeListView(RetrieveAPIView):
    """ how all post like """

    queryset = WomanLike.objects.all()
    serializer_class = PostLikeListSerializer


class CommentLikeAPIView(BaseAPIView, ListCreateAPIView):
    """ put like to comment """

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeCreateSerializer
    pagination_class = PostPageNumberPagination


class LikeCommentAPIView(BaseAPIView, ListAPIView):
    """ put like to comment """

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeViewSerializer


class AuthorListAPIView(ListAPIView):
    """ all authors """

    queryset = Author.objects.all() 
    serializer_class = AuthoeSerializer
    pagination_class = pagination.LimitOffsetPagination


class AuthorDetailAPIView(RetrieveAPIView):
    """ detail authors """

    queryset = Author.objects.all() 
    serializer_class = AuthoeSerializer
    lookup_url_kwarg = "author_id"


class LikeCommentDetailAPIView(RetrieveAPIView):
    """ like detailed """

    queryset = LikedComment.objects.all()
    serializer_class = CommentLikeListSerializer
    lookup_url_kwarg = "like_id"
