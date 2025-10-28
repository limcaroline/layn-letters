from django.urls import path
from .views import (
    BudgetList, BudgetDetail, BudgetCreate,
    BudgetUpdate, BudgetDelete
)

app_name = "budgets"

urlpatterns = [
    path("", BudgetList.as_view(), name="list"),
    path("create/", BudgetCreate.as_view(), name="create"),
    path("<int:pk>/", BudgetDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", BudgetUpdate.as_view(), name="edit"),
    path("<int:pk>/delete/", BudgetDelete.as_view(), name="delete"),
]
