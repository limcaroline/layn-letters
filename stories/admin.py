from django.contrib import admin
from .models import Category, Story, Comment, Vote


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created")
    list_filter = ("status", "category", "created")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Comment)
admin.site.register(Vote)
