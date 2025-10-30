from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Itinerary(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
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
            self.slug = slugify(self.title)[:170]
        super().save(*args, **kwargs)


class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="items"
    )
    day = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    notes = models.CharField(max_length=240, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
