from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Story, Vote, Comment, CommentVote
from django.db.models import Sum
from core.utils import is_site_owner


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        score = self.object.votes.aggregate(total=Sum("value"))["total"] or 0
        ctx["score"] = score
        return ctx


class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        return is_site_owner(self.request.user)


class AuthorRequired(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class StoryCreate(LoginRequiredMixin, OwnerOnly, CreateView):
    model = Story
    fields = ["title", "content", "category", "cover_image", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StoryUpdate(LoginRequiredMixin, AuthorRequired, OwnerOnly, UpdateView):
    model = Story
    fields = ["title", "content", "category", "cover_image", "status"]


class StoryDelete(LoginRequiredMixin, AuthorRequired, OwnerOnly, DeleteView):
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


class CommentEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["body"]
    def test_func(self): return self.get_object().author == self.request.user
    def get_success_url(self): return self.object.story.get_absolute_url()


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    def test_func(self):
        c = self.get_object()
        return c.author == self.request.user or is_site_owner(self.request.user)
    def get_success_url(self): return self.object.story.get_absolute_url()


class CommentVoteToggle(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        value = int(request.POST.get("value", 1))
        vote, created = CommentVote.objects.get_or_create(
            comment=comment, user=request.user, defaults={"value": value}
        )
        if not created:
            vote.value = value
            vote.save()
        score = comment.votes.aggregate(total=Sum("value"))["total"] or 0
        return JsonResponse({"score": score})
