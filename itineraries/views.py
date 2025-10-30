from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.shortcuts import redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Itinerary
from .forms import ItineraryForm, ItemFormSet


# Create your views here.
class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.is_staff
        )


class ItineraryList(ListView):
    model = Itinerary
    template_name = "itineraries/itinerary_list.html"
    paginate_by = 10


class ItineraryDetail(DetailView):
    model = Itinerary
    template_name = "itineraries/itinerary_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ItineraryCreate(LoginRequiredMixin, OwnerOnly, CreateView):
    model = Itinerary
    form_class = ItineraryForm
    template_name = "itineraries/itinerary_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        formset = ItemFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return redirect(self.object.get_absolute_url())
        ctx = self.get_context_data(form=form)
        ctx["formset"] = formset
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"] = ItemFormSet()
        return ctx


class ItineraryUpdate(LoginRequiredMixin, OwnerOnly, UpdateView):
    model = Itinerary
    form_class = ItineraryForm
    template_name = "itineraries/itinerary_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"] = ItemFormSet(instance=self.object)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ItemFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.object.get_absolute_url())
        ctx = self.get_context_data(form=form)
        ctx["formset"] = formset
        return self.render_to_response(ctx)


class ItineraryDelete(LoginRequiredMixin, OwnerOnly, DeleteView):
    model = Itinerary
    template_name = "itineraries/itinerary_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("itineraries:list")
