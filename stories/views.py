from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Story, Vote


# Create your views here.
class StoryList(ListView):
    model = Story
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("author", "category")
        return qs.filter(status=Story.PUBLISHED)


class StoryDetail(DetailView):
    model = Story
    slug_field = "slug"


class StoryCreate(LoginRequiredMixin, CreateView):
    model = Story
    fields = ["title", "content", "category", "cover_image", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorRequired(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class StoryUpdate(LoginRequiredMixin, AuthorRequired, UpdateView):
    model = Story
    fields = ["title", "content", "category", "cover_image", "status"]


class StoryDelete(LoginRequiredMixin, AuthorRequired, DeleteView):
    model = Story
    success_url = reverse_lazy("stories:list")


class VoteToggle(LoginRequiredMixin, View):
    def post(self, request, slug):
        story = Story.objects.get(slug=slug)
        value = int(request.POST.get("value", 1))
        vote, created = Vote.objects.get_or_create(
            story=story, user=request.user, defaults={"value": value}
        )
        if not created:
            vote.value = value
            vote.save()
        score = story.votes.aggregate(total=Sum("value"))["total"] or 0
        return JsonResponse({"score": score})
