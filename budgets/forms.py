from django import forms
from .models import BudgetItem


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = [
            "name", "category", "day", "quantity", "unit_cost", "notes",
        ]
        widgets = {
            "quantity": forms.NumberInput(
                attrs={"step": "0.01", "data-bqty": "1"}
            ),
            "unit_cost": forms.NumberInput(
                attrs={"step": "0.01", "data-bunit": "1"}
            ),
        }
