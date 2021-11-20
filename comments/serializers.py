from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)
from store.models import (
    LikedComment,
    WomanComment,
    WomanLike,
)
from accounts.serializers import UserDetailSerializer
from store.models import Woman
from rest_framework import serializers


class CommentPostSerializer(ModelSerializer):
    """post comment to news"""

    url = HyperlinkedIdentityField(view_name="comment-details")

    class Meta:
        model = WomanComment
        fields = "id", "url"


class CommentLikeViewSerializer(ModelSerializer):
    class Meta:
        model = LikedComment
        exclude = ("choice",)


class CommentLikeDetailSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name="detail-likes")

    class Meta:
        model = LikedComment
        fields = ("id", "url")


class CommentLikeDetaliSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name="detail-comment-likes")

    class Meta:
        model = WomanLike
        fields = ("id", "url")


class CommentAllSerializer(ModelSerializer):
    """All information about comment
    in case if we wanna see what we destroy"""

    post = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)
    api_url = SerializerMethodField()

    class Meta:
        model = WomanComment
        fields = ("id", "comment", "post", "user", "likes_comment", "api_url")

    # def get_user(self, instance):
    #     return instance.user.username

    def get_post(self, instance):
        return instance.post.title

    def get_api_url(self, instance):
        return instance.get_api_url()

    likes_comment = CommentLikeDetaliSerializer(many=True)


class CommentPosListSerializer(ModelSerializer):
    """post comment to news"""

    post = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = WomanComment
        fields = ("id", "post", "user", "comment", "likes_comment")

    # def get_user(self, instance):
    #     return instance.user.username

    def get_post(self, instance):
        return instance.post.title

    likes_comment = CommentLikeDetaliSerializer(many=True)


class CommentLikeCreateSerializer(ModelSerializer):
    class Meta:
        model = LikedComment
        fields = [
            "is_liked",
            # "post_comment",
            # "user"
        ]

    def create(self, validated_data):

        post_comment = (
            WomanComment.objects.get(
                pk=int(self.context["request"].path.split("/")[-3])
            ),
        )
        user = (self.context["request"].user,)

        is_like = LikedComment.objects.filter(
            post_comment=post_comment[0],
            user=user[0],
        )
        id_pk = is_like.first().pk if is_like else None
        if is_like and is_like.first().is_liked:
            is_like.delete()
            return LikedComment.objects.create(
                id=id_pk, post_comment=post_comment[0], user=user[0], is_liked=False
            )
        else:
            is_like.delete()
            return LikedComment.objects.create(
                id=id_pk, post_comment=post_comment[0], user=user[0], is_liked=True
            )


class PostCommentCreateAPIView(ModelSerializer):
    class Meta:
        model = WomanComment
        fields = [
            # "post",
            # "user",
            "comment",
        ]

    def create(self, validated_data):

        comment = validated_data["comment"]

        return WomanComment.objects.create(
            post=Woman.objects.get(slug=self.context["request"].path.split("/")[-3]),
            user=self.context["request"].user,
            comment=comment,
        )


class CommentLikeListSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    post_comment = serializers.SlugRelatedField(slug_field="comment", read_only=True)
    get_api_url = SerializerMethodField()

    class Meta:
        model = LikedComment
        fields = "post_comment", "user", "choice", "get_api_url"

    # def get_user(self, instance):
    #     return instance.user.username

    def get_post(self, instance):
        return instance.post.title

    def get_api_url(self, instance):
        return instance.get_api_url()
