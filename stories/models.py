from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Story(models.Model):
    DRAFT, PUBLISHED = "draft", "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    cover_image = models.ImageField(
        upload_to="stories/covers/", blank=True, null=True
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PUBLISHED
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:160]
            self.slug = base
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("stories:detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    body = models.TextField(max_length=1000)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE,
        related_name="replies"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    value = models.SmallIntegerField(choices=[(-1, "Down"), (1, "Up")])

    class Meta:
        unique_together = ("story", "user")


class CommentVote(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    value = models.SmallIntegerField(choices=[(-1, "Down"), (1, "Up")])

    class Meta:
        unique_together = ("comment", "user")
