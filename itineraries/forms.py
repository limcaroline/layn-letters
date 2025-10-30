from django import forms
from django.forms import inlineformset_factory
from .models import Itinerary, ItineraryItem


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ["title", "days", "notes"]


class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = ["day", "title", "location", "notes", "start_time", "cost"]
        widgets = {"cost": forms.NumberInput(attrs={"step": "0.01"})}


ItemFormSet = inlineformset_factory(
    Itinerary, ItineraryItem, form=ItineraryItemForm, extra=4, can_delete=True
)
