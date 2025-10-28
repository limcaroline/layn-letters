from django.contrib import admin
from .models import Budget, BudgetItem


# Register your models here.
class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "currency", "created")
    inlines = [BudgetItemInline]


admin.site.register(BudgetItem)
