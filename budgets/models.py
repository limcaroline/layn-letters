from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Budget(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    currency = models.CharField(max_length=8, default="USD")
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("budgets:detail", args=[self.pk])


class BudgetItem(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=60, blank=True)
    day = models.PositiveIntegerField(default=1)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    notes = models.CharField(max_length=200, blank=True)

    def line_total(self):
        return (self.quantity or 0) * (self.unit_cost or 0)
