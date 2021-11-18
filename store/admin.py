from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from django.db.models import F
# Register your models here.


class PostAdminForm(forms.ModelForm):

    """ Visual redactor depicter """

    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Woman
        fields = '__all__'
        skin = 'moono-dark';



class WomanImageInline(admin.TabularInline):
    model = WomanImage
    extra = 0
    show_change_link = True

class WomanAdmin(admin.ModelAdmin):

    form = PostAdminForm
    list_display = ("id", "title", "author",
                    "cat","is_published","creation_date", "updation_date")  # that's will be displayed in django-admin
    list_display_links = ("id", "title")  # this ones we can click like links
    search_fields = ("title", "content")
    list_editable = ["is_published"]
    prepopulated_fields = {"slug": ("title",)}
    fields = ("title", "slug", "content",  "photo" , "get_photo" , "is_published", 
                     "cat", "author" ,("updation_date", "creation_date"),)
    readonly_fields = ("get_photo","updation_date", "creation_date",)
    list_per_page = 200 #max post per page
    list_max_show_all = 50 #max posts after clicking on hyperref
    view_on_site = True
    empty_value_display = 'unknown' #empty one of values

    # inlines = [WomanImageInline] #lwt us add a couple of photos to each post

    @admin.display(description = "Views") #to depict it in form in admin as lable to field
    def get_count_views(self, obj):
        if obj:
            return obj.get_view_count()

    @admin.display(description = "View photo") #to depict it in form in admin as lable to field
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=300 >") #show picture in form
        return "empty"   
       

    def unpublish(modeladmin, request, queryset):
        """ publish or unpublish action """

        for w in queryset:
            if w.is_published:
                w.is_published = False
            else:
                w.is_published = True

            w.save()    
            modeladmin.message_user(request, 'Successfully changed publish type')

    unpublish.short_description = 'Change publish'
    unpublish.allowed_permissions = ("change",)

    actions = (unpublish, )
    save_on_top = True


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "age", "rate")
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "age", "rate")


    def get_ico(self, obj):
        if obj.ico:
            return mark_safe(f"<img src='{obj.ico.url}' width=150>")

    get_ico.short_description = "icon"        



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "ico", "get_ico")
    readonly_fields = ("get_ico",)


    def get_ico(self, obj):
        if obj.ico:
            return mark_safe(f"<img src='{obj.ico.url}' width=150>")

    get_ico.short_description = "icon"        


class IpModelAdmin(admin.ModelAdmin):
    list_display = ("post_news" ,"ip")
    fields = ("post_news" ,"ip")
    readonly_fields = ("ip",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star",)
    fields = ("star",)


class WomanCommentAdmin(admin.ModelAdmin):

    list_display = ('id','user', 'comment','get_post_title',"creation_date",)
    list_display_links = ('id', 'user', "comment", "get_post_title")
    search_fields = ('user',)
    fields = ("user", "comment", "post", "creation_date")
    readonly_fields = ("creation_date",)
    autocomplete_fields = ['post']

    def get_post_title(self, obj):
        if obj.post:
            return mark_safe(f" <p> {obj.post.slug} </p> ")


@admin.register(WomanImage)
class WomanImageAdmin(admin.ModelAdmin):
    list_display = ('id','images',)
    list_display_links = ('id', 'images')
    search_fields = ('id',)
    fields = ('id','images',)


class LikedCommentAdmin(admin.ModelAdmin):
    list_display = ('id','post_comment', "user")
    list_display_links = ('id', 'post_comment')
    search_fields = ('id',)

admin.site.register(Woman, WomanAdmin)  # in order to show it in django-admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(WomanComment, WomanCommentAdmin)
admin.site.register(WomanLike)
admin.site.register(LikedComment, LikedCommentAdmin)
admin.site.register(IpModel, IpModelAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.site_header = "Django Admin" #header of site name
admin.site.site_title = "Admin" #admin title name
admin.site.index_title = "Admin panel"

admin.site.empty_value_display = 'empty'  


