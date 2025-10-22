from django.shortcuts import render
from django.db.models import Sum
from stories.models import Story


# Create your views here.
def home(request):
    qs = Story.objects.filter(status=Story.PUBLISHED).select_related(
        "author", "category"
    )
    latest = qs.order_by("-created")[:6]
    trending = (
        qs.annotate(score=Sum("votes__value"))
          .order_by("-score", "-created")[:6]
    )
    return render(
        request,
        "core/home.html",
        {"latest": latest, "trending": trending},
    )
