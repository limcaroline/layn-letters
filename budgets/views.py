from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import redirect
from .models import Budget, BudgetItem
from .forms import BudgetItemForm


# Create your views here.
class AuthorOnly(UserPassesTestMixin):
    def test_func(self):
        obj = getattr(self, "object", None)
        if obj is None and hasattr(self, "get_object"):
            obj = self.get_object()
        if not obj or not self.request.user.is_authenticated:
            return False
        return (obj.author == self.request.user or
                self.request.user.is_staff)


ItemFormSet = inlineformset_factory(
    Budget,
    BudgetItem,
    form=BudgetItemForm,
    fields=["name", "category", "day", "quantity", "unit_cost", "notes"],
    extra=4,
    can_delete=True,
)


class BudgetList(ListView):
    model = Budget
    template_name = "budgets/budget_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("author")
        if (
            self.request.GET.get("mine") == "1"
            and self.request.user.is_authenticated
        ):
            qs = qs.filter(author=self.request.user)
        return qs


class BudgetDetail(DetailView):
    model = Budget
    template_name = "budgets/budget_detail.html"


class BudgetCreate(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ["title", "currency", "notes"]
    template_name = "budgets/budget_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        resp = super().form_valid(form)
        return resp

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formset"] = ItemFormSet()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            budget = form.save(commit=False)
            budget.author = request.user
            budget.save()
            fs = ItemFormSet(request.POST, instance=budget)
            if fs.is_valid():
                fs.save()
            return redirect(budget.get_absolute_url())
        ctx = self.get_context_data(form=form)
        ctx["formset"] = formset
        return self.render_to_response(ctx)


class BudgetUpdate(LoginRequiredMixin, AuthorOnly, UpdateView):
    model = Budget
    fields = ["title", "currency", "notes"]
    template_name = "budgets/budget_form.html"

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


class BudgetDelete(LoginRequiredMixin, AuthorOnly, DeleteView):
    model = Budget
    success_url = reverse_lazy("budgets:list")
    template_name = "budgets/budget_confirm_delete.html"
