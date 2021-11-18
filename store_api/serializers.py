from django.contrib.auth.models import User
from django.db import models
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import (
    ModelSerializer, 
    HyperlinkedIdentityField, 
    SerializerMethodField)
from rest_framework import  serializers
from store.models import Author, LikedComment, Rating, Woman, Category, WomanComment, WomanLike
from django.utils.html import strip_tags


class CommentPostSerializer(ModelSerializer):
    """ post comment to news """


    class Meta:
        model = WomanComment
        fields = "__all__"

    read_only_fields = [
        "user",
        "post"
    ]



class CommentLikeViewSerializer(ModelSerializer):

    class Meta:
        model = LikedComment
        exclude = "choice", 


class CommentAllSerializer(ModelSerializer):
    """ All information about comment
    in case if we wanna see what we destroy """

    post = SerializerMethodField()  
    user = SerializerMethodField()

    class Meta:
        model = WomanComment
        fields = ("id",
                "comment", 
                "post",
                "user",
                "likes_comment"
        )
    def get_user(self, instance):
        return instance.user.username
        
    def get_post(self, instance):
        return instance.post.title

    likes_comment = CommentLikeViewSerializer(many=True)


class CommentPosListSerializer(ModelSerializer):
    """ post comment to news """

    post = SerializerMethodField()
    user = SerializerMethodField()
    class Meta:
        model = WomanComment
        fields = (
            "id",
            "post",
            "user",
            "comment",
            "likes_comment"
        )

    def get_user(self, instance):
        return instance.user.username
        
    def get_post(self, instance):
        return instance.post.title

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


class PostLikeUpdateSerializer(ModelSerializer):

    post = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = WomanLike
        fields = ("id", "post" ,"user", "rating") 

    def get_user(self, instance):
        return instance.user.username

    def get_post(self, instance):
        return instance.post.title

class WomanSerializer(ModelSerializer):
    
    category = HyperlinkedIdentityField(
        view_name="list-category-special",
        lookup_field = "cat_id"
    )
    author = HyperlinkedIdentityField(
        view_name="authors-detail",
        lookup_field = "author_id"
    )
    
    image = SerializerMethodField()
    all_comments = CommentPostSerializer(many=True)
    likes = PostLikeUpdateSerializer(many=True)

    class Meta:
        model = Woman
        fields = [
            'title',
            'content',
            "category",
            "author", 
            "all_comments",
            "likes",
            "image"
        ]

    def get_image(self, instance):
        try:
            image = instance.photo.url
        except:
            image = None
        return image    
        
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

    image = SerializerMethodField()    

    class Meta:
        model = Woman
        fields = ("title", "slug", "content", "cat", "author", "all_comments", "image", "is_published")    

    def get_image(self, instance):
        try:
            image = instance.photo.url
        except:
            image = None
        return image        

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data
    

class PostLikeCreateSerializer(ModelSerializer):

    class Meta:
        model = WomanLike
        fields = "rating",     


    def create(self, validated_data):

        post = Woman.objects.get(slug=self.context["request"].path.split("/")[-3]),
        user = self.context["request"].user,
        rating = validated_data["rating"]

        like = WomanLike.objects.filter(
            post=post[0],
            user = user[0]
        )
        id_pk = like.first().pk if like else None
        if like:
             
            like.delete()
        return WomanLike.objects.create(
            id = id_pk,
            post=post[0],
            user = user[0],
            rating = rating
        )
        

class PostLikeListSerializer(ModelSerializer):

    user = SerializerMethodField()
    post = SerializerMethodField()
    class Meta:
        model = WomanLike
        fields = "__all__"

    def get_user(self, instance):
        return instance.user.username 

    def get_post(self, instance):
        return instance.post.title          


class CommentLikeListSerializer(ModelSerializer):
    user = SerializerMethodField()
    post = serializers.SlugRelatedField(slug_field="title", read_only = True)
    class Meta:
        model = LikedComment
        fields = "__all__"

    def get_user(self, instance):
        return instance.user.username

    def get_post(self, instance):
        return instance.post.title    

class CommentLikeCreateSerializer(ModelSerializer):

    class Meta:
        model = LikedComment
        fields = [
            "is_liked",
            # "post_comment",
            # "user"
        ]

    def create(self, validated_data):

        post_comment = WomanComment.objects.get(pk=int(self.context["request"].path.split("/")[-3])),
        user = self.context["request"].user,

        is_like = LikedComment.objects.filter(
            post_comment=post_comment[0],
            user = user[0],
        )
        id_pk = is_like.first().pk if is_like else None
        if is_like and is_like.first().is_liked:
            is_like.delete()
            return LikedComment.objects.create(
                id = id_pk,
                post_comment=post_comment[0],
                user = user[0],
                is_liked = False
            )
        else:   
            is_like.delete()
            return LikedComment.objects.create(
                id = id_pk,
                post_comment=post_comment[0],
                user = user[0],
                is_liked = True
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
            post = Woman.objects.get(slug=self.context["request"].path.split("/")[-3]),
            user = self.context["request"].user,
            comment = comment
        )

class AuthoeSerializer(ModelSerializer):

    class Meta:
        model = Author
        exclude = "slug"  ,     