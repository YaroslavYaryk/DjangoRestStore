from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)
from rest_framework import serializers
from store.models import (
    Author,
    LikedComment,
    Rating,
    Woman,
    Category,
    WomanComment,
    WomanLike,
)
from comments.serializers import CommentPostSerializer
from django.utils.html import strip_tags
from accounts.serializers import UserDetailSerializer


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class AuthorViewSerializer(ModelSerializer):
    """show all actors"""

    class Meta:

        model = Author
        fields = ("name", "age", "rate")


class CatSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class PostLikeUpdateSerializer(ModelSerializer):

    post = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = WomanLike
        fields = ("id", "post", "user", "rating")

    def get_user(self, instance):
        return instance.user.username

    def get_post(self, instance):
        return instance.post.title


class PostLikeDetaliSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name="detail-likes")

    class Meta:
        model = WomanLike
        fields = ("id", "url")


class WomanSerializer(ModelSerializer):

    category = HyperlinkedIdentityField(
        view_name="list-category-special", lookup_field="cat_id"
    )
    author = HyperlinkedIdentityField(
        view_name="authors-detail", lookup_field="author_id"
    )

    image = SerializerMethodField()
    all_comments = CommentPostSerializer(many=True)
    likes = PostLikeDetaliSerializer(many=True)

    class Meta:
        model = Woman
        fields = [
            "title",
            "content",
            "category",
            "author",
            "all_comments",
            "likes",
            "image",
        ]

    def get_image(self, instance):
        try:
            image = instance.photo.url
        except Exception:
            image = None
        return image

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["content"] = strip_tags(instance.content)
        return data


class WomanCreateSerializer(ModelSerializer):
    class Meta:
        model = Woman
        fields = ["title", "content", "cat", "author"]


class WomanSpecialSerializer(ModelSerializer):

    image = SerializerMethodField()

    class Meta:
        model = Woman
        fields = (
            "title",
            "slug",
            "content",
            "cat",
            "author",
            "all_comments",
            "image",
            "is_published",
        )

    def get_image(self, instance):
        try:
            image = instance.photo.url
        except Exception:
            image = None
        return image

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["content"] = strip_tags(instance.content)
        return data

    all_comments = CommentPostSerializer(many=True)
    cat = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)


class WomanSpecialUpdateSerializer(ModelSerializer):
    class Meta:
        model = Woman
        fields = ("title", "slug", "content", "cat", "author", "is_published")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["content"] = strip_tags(instance.content)
        return data


class PostLikeCreateSerializer(ModelSerializer):
    class Meta:
        model = WomanLike
        fields = ("rating",)

    def create(self, validated_data):

        post = (Woman.objects.get(slug=self.context["request"].path.split("/")[-3]),)
        user = (self.context["request"].user,)
        rating = validated_data["rating"]

        like = WomanLike.objects.filter(post=post[0], user=user[0])
        id_pk = like.first().pk if like else None
        if like:

            like.delete()
        return WomanLike.objects.create(
            id=id_pk, post=post[0], user=user[0], rating=rating
        )


class PostLikeListSerializer(ModelSerializer):

    user = UserDetailSerializer(read_only=True)
    post = SerializerMethodField()
    get_api_url = SerializerMethodField()

    class Meta:
        model = WomanLike
        fields = "post", "user", "rating", "get_api_url"

    # def get_user(self, instance):
    #     return instance.user.username

    def get_post(self, instance):
        return instance.post.title

    def get_api_url(self, instance):
        return instance.get_api_url()


class AuthoeSerializer(ModelSerializer):
    class Meta:
        model = Author
        exclude = ("slug",)
