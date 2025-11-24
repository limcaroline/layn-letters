from decimal import Decimal
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Sum, F, DecimalField, ExpressionWrapper


# Create your models here.
CURRENCY_CHOICES = [
    ("SEK", "SEK — Swedish krona"),
    ("USD", "USD — US dollar"),
    ("EUR", "EUR — Euro"),
    ("PHP", "PHP — Philippine peso"),
    ("GBP", "GBP — British pound"),
    ("JPY", "JPY — Japanese yen"),
    ("CNY", "CNY — Chinese yuan"),
    ("AUD", "AUD — Australian dollar"),
    ("CAD", "CAD — Canadian dollar"),
    ("CHF", "CHF — Swiss franc"),
    ("NZD", "NZD — New Zealand dollar"),
    ]


class Budget(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    currency = models.CharField(
        max_length=8, default="SEK", choices=CURRENCY_CHOICES
    )
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("budgets:detail", args=[self.pk])

    @property
    def total_amount(self):
        agg = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("unit_cost"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
        )
        return agg["total"] or Decimal("0")


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

    @property
    def line_total(self):
        q = self.quantity or Decimal("0")
        p = self.unit_cost or Decimal("0")
        return q * p
