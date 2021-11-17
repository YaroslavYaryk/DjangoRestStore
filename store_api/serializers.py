from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework import  serializers
from store.models import Author, LikedComment, Rating, Woman, Category, WomanComment, WomanLike
from django.utils.html import strip_tags


class CommentPostSerializer(ModelSerializer):
    """ post comment to news """

    class Meta:
        model = WomanComment
        exclude = ("post",)


class CommentAllSerializer(ModelSerializer):
    """ All information about comment
    in case if we wanna see what we destroy """

    post = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = WomanComment
        fields = "__all__"


class CommentLikeViewSerializer(ModelSerializer):

    class Meta:
        model = LikedComment
        exclude = "id", "choice"


class CommentPosListSerializer(ModelSerializer):
    """ post comment to news """

    class Meta:
        model = WomanComment
        fields = (
            "id",
            "post",
            "username",
            "comment",
            "likes_comment"
        )
    likes_comment = CommentLikeViewSerializer(many=True)

class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = "__all__"


class AuthorViewSerializer(ModelSerializer):
    """ show all actors """
    
    class Meta:

        model = Author   
        fields = ("name", "age", "rate")


class CatSerializer(ModelSerializer):
    

    class Meta:
        model = Category
        fields = [
            'id', 
            'name', 
            'slug', 
        ]


class WomanSerializer(ModelSerializer):
    
    category = HyperlinkedIdentityField(
        view_name="list-category-special",
        lookup_field = "cat_id"
    )
    author = HyperlinkedIdentityField(
        view_name="authors-detail",
        lookup_field = "author_id"
    )
    all_comments = CommentPostSerializer(many=True)
    likes = HyperlinkedIdentityField(
        view_name="detail-likes",
        # lookup_field = ""
    )

    class Meta:
        model = Woman
        fields = [
            'title',
            'content',
            "category",
            "author", 
            "all_comments",
            "likes",
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data    


class WomanCreateSerializer(ModelSerializer):
    
    class Meta:
        model = Woman
        fields = [
            'title', 
            'content', 
            'cat', 
            "author"
        ]


class WomanSpecialSerializer(ModelSerializer):
    
    class Meta:
        model = Woman
        fields = ("title", "slug", "content", "cat", "author", "all_comments",  "is_published")    


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data  

    all_comments = CommentPostSerializer(many=True)
    cat = serializers.SlugRelatedField(slug_field="name", read_only = True)
    author = serializers.SlugRelatedField(slug_field="name", read_only = True)       


class WomanSpecialUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = Woman
        fields = ("title", "slug", "content", "cat",  "author",  "is_published")    

    

class PostLikeCreateSerializer(ModelSerializer):

    class Meta:
        model = WomanLike
        exclude = ["ip"]    


    def create(self, validated_data):
        validated_data['ip'] = self.context.get('request').META.get("REMOTE_ADDR")
        like = WomanLike.objects.filter(
            post=validated_data["post"],
            ip = validated_data["ip"]
        )
        if like:
           like.delete()
        return WomanLike.objects.create(**validated_data)
        

class PostLikeListSerializer(ModelSerializer):

    class Meta:
        model = WomanLike
        exclude = ["ip"]    
     


class PostLikeUpdateSerializer(ModelSerializer):

    class Meta:
        model = WomanLike
        exclude = ["ip"] 



class CommentLikeListSerializer(ModelSerializer):

    class Meta:
        model = LikedComment
        fields = "__all__"

class CommentLikeCreateSerializer(ModelSerializer):

    class Meta:
        model = LikedComment
        fields = [
            "is_liked",
            "post_comment",
            "user"
        ]

    def create(self, validated_data):

        post_comment=validated_data["post_comment"]
        user = validated_data["user"]
        is_like = LikedComment.objects.get(
            post_comment=post_comment,
            user = user,
        )
        id_pk = is_like.pk
        if is_like and is_like.is_liked:
            is_like.delete()
            return LikedComment.objects.create(
                id = id_pk,
                post_comment=post_comment,
                user = user,
                is_liked = False
            )
        else:   
            is_like.delete()
            return LikedComment.objects.create(
                id = id_pk,
                post_comment=post_comment,
                user = user,
                is_liked = True
            )


class PostCommentCreateAPIView(ModelSerializer):

    class Meta:
        model = WomanComment
        fields = [
            "post",
            "username",
            "comment",
        ]

class AuthoeSerializer(ModelSerializer):

    class Meta:
        model = Author
        exclude = "slug"  ,     