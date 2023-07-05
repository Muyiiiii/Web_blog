from django.contrib import admin
from .models import Moment, User, Contact, Comment, Video


# Register your models here.

@admin.register(Moment)
class MomentManager(admin.ModelAdmin):
    list_display = ['title', 'is_valid']
    search_fields = ['title']
    pass


@admin.register(User)
class UserManager(admin.ModelAdmin):
    list_display = ['name', 'if_login']
    search_fields = ['name']
    pass


@admin.register(Contact)
class ContactManager(admin.ModelAdmin):
    list_display = ['real_name', 'subject', 'date']
    search_fields = ['real_name']
    pass


@admin.register(Comment)
class CommentManager(admin.ModelAdmin):
    list_display = ['moment_id', 'author_name', 'date']
    search_fields = ['author_name']
    pass


@admin.register(Video)
class CommentManager(admin.ModelAdmin):
    list_display = ['video_name', 'video_file']
    search_fields = ['video_name']
    pass
