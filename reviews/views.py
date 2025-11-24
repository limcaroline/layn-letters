from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from core.utils import is_site_owner
from .forms import ReviewForm, ReviewCommentForm, PlaceForm
from .models import Review, Place, ReviewComment, ReviewCommentVote


# ---------- Mixins ----------

class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        return is_site_owner(self.request.user)


class AuthorRequired(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


# ---------- Review CRUD (owner-only) ----------

class ReviewList(ListView):
    model = Review
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("author", "place")
        place = self.request.GET.get("place")
        if place:
            qs = qs.filter(place__name__icontains=place)
        return qs


class ReviewDetail(DetailView):
    model = Review

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = ReviewCommentForm()
        ctx["comments"] = (
            ReviewComment.objects.filter(review=self.object)
            .select_related("author")
            .annotate(score=Sum("votes__value"))
            .order_by("-created")
        )
        ctx["place_avg"] = (
            Review.objects.filter(place=self.object.place)
            .aggregate(avg=Avg("rating"))["avg"]
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("account_login")
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            cm = form.save(commit=False)
            cm.review = self.object
            cm.author = request.user
            cm.save()
        return redirect(self.object.get_absolute_url())


class ReviewCreate(LoginRequiredMixin, OwnerOnly, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewUpdate(LoginRequiredMixin, OwnerOnly, UpdateView):
    model = Review
    form_class = ReviewForm


class ReviewDelete(LoginRequiredMixin, OwnerOnly, DeleteView):
    model = Review
    success_url = reverse_lazy("reviews:list")


# ---------- Optional Place create (owner-only) ----------

class PlaceCreate(LoginRequiredMixin, OwnerOnly, CreateView):
    model = Place
    form_class = PlaceForm
    success_url = reverse_lazy("reviews:list")


# ---------- Comment edit/delete and vote ----------

class ReviewCommentEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReviewComment
    fields = ["body"]

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.review.get_absolute_url()


class ReviewCommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReviewComment

    def test_func(self):
        cm = self.get_object()
        return cm.author == self.request.user or is_site_owner(
            self.request.user
        )

    def get_success_url(self):
        return self.object.review.get_absolute_url()


class ReviewCommentVoteToggle(LoginRequiredMixin, View):
    def post(self, request, pk):
        cm = get_object_or_404(ReviewComment, pk=pk)
        value = int(request.POST.get("value", 1))

        vote, created = ReviewCommentVote.objects.get_or_create(
            comment=cm,
            user=request.user,
            defaults={"value": 0},
        )

        current = 0 if created else vote.value

        if value == 1:
            # upvote: increase by 1 and max is +1
            new = min(current + 1, 1)
        elif value == -1:
            # downvote: decrease by 1 and min is -1
            new = max(current - 1, -1)
        else:
            new = current

        if new == 0:
            if not created:
                vote.delete()
        else:
            vote.value = new
            vote.save()

        return redirect(cm.review.get_absolute_url())


