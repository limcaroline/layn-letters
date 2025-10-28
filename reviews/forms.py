from django import forms
from .models import Review, ReviewComment, Place


# Create your models here.
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["place", "title", "rating", "body", "visited_on"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name", "city", "country", "kind"]


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3,
                                          "placeholder": "Add a comment…"})
        }
        labels = {"body": ""}
