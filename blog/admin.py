from django.contrib import admin
from .models import Post, Author, Tag, Comment
from django.contrib.admin.utils import flatten_fieldsets


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter = (
        "author",
        "tags",
        "date",
    )
    list_display = (
        "title",
        "date",
        "author",
    )
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")

    readonly_fields = [i.name for i in Comment._meta.get_fields()]


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
