from datetime import date
from django import forms
from .models import Review, ReviewComment, Place


# Create your models here.
class ReviewForm(forms.ModelForm):
    visited_on = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={
            "type": "date",
            "placeholder": "YYYY-MM-DD",
            "title": "YYYY-MM-DD",
        }),
    )

    class Meta:
        model = Review
        fields = ["place", "title", "rating", "body", "visited_on"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today_iso = date.today().isoformat()
        self.fields["visited_on"].widget.attrs["max"] = today_iso

    def clean_visited_on(self):
        d = self.cleaned_data.get("visited_on")
        if d and d > date.today():
            raise forms.ValidationError(
                "Visited date cannot be in the future."
            )
        return d


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
