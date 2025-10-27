from django.contrib import admin
from .models import Place, Review, ReviewComment, ReviewCommentVote


# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "kind")
    list_filter = ("kind", "country", "city")
    search_fields = ("name", "city", "country")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "place", "author", "rating", "created")
    list_filter = ("rating", "place")
    search_fields = ("title", "body")


admin.site.register(ReviewComment)
admin.site.register(ReviewCommentVote)
