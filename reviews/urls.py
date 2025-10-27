from django.conf import settings
from django.db import models
from django.urls import reverse


class Place(models.Model):
    RESTAURANT = "restaurant"
    ATTRACTION = "attraction"
    OTHER = "other"
    KIND_CHOICES = [
        (RESTAURANT, "Restaurant"),
        (ATTRACTION, "Attraction"),
        (OTHER, "Other"),
    ]

    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    kind = models.CharField(
        max_length=20, choices=KIND_CHOICES, default=OTHER
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def avg_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"]


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField()  # 1–5
    body = models.TextField(blank=True)
    visited_on = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.place} — {self.title}"

    def get_absolute_url(self):
        return reverse("reviews:detail", args=[self.pk])


class ReviewComment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReviewCommentVote(models.Model):
    comment = models.ForeignKey(
        ReviewComment, on_delete=models.CASCADE, related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    value = models.SmallIntegerField(choices=[(-1, "Down"), (1, "Up")])

    class Meta:
        unique_together = ("comment", "user")
