from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
def unique_slugify(instance, value, slug_field="slug", max_len=170):
    base = slugify(value)[:max_len] or "itinerary"
    slug = base
    Model = instance.__class__
    n = 2
    while Model.objects.filter(**{slug_field: slug}).exists():
        suf = f"-{n}"
        slug = f"{base[: max_len - len(suf)]}{suf}"
        n += 1
    return slug


class Itinerary(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    days = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("itineraries:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:160]
            slug = base or "itinerary"
            counter = 1

            from .models import Itinerary
            Model = type(self)

            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                suffix = f"-{counter}"
                slug = f"{base[:160 - len(suffix)]}{suffix}"

            self.slug = slug

        super().save(*args, **kwargs)


class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="items"
    )
    day = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    notes = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["day", "id"]
