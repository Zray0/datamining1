
from django.contrib import admin
from .models import AssocRule

@admin.register(AssocRule)
class AssocRuleAdmin(admin.ModelAdmin):
    list_display = ("show_antecedents","show_consequents","support","confidence","lift")
    search_fields = ("antecedents","consequents")
    ordering = ("-lift","-confidence","-support")
    list_per_page = 50

    def show_antecedents(self, obj): return ", ".join(obj.antecedents)
    def show_consequents(self, obj): return ", ".join(obj.consequents)
