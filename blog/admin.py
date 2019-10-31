from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'user', 'click_count', 'date_publish', 'created_time',)
    list_per_page = 50
    ordering = ('-date_publish',)

    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/kindeditor-all.js',
            '/static/js/kindeditor/config.js'
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index',)
    ordering = ('index', 'id',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-id',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'content', 'date_publish', 'pid',)
    list_per_page = 50
    list_display_links = ('id', 'content',)
    ordering = ['-date_publish', ]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    ordering = ['index', 'id', ]


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    ordering = ['index', 'id']
