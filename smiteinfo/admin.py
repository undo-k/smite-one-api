from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import God, Item, Match, MatchPlayer, MatchPlayerDetail


class MatchPlayerAdminForm(ModelForm):
    class Meta:
        model = MatchPlayer
        fields = "__all__"
        widgets = {
            "items": FilteredSelectMultiple("Items", is_stacked=False),
        }


class MatchPlayerDetailInline(admin.StackedInline):
    model = MatchPlayerDetail
    can_delete = False


class MatchPlayerAdmin(admin.ModelAdmin):
    form = MatchPlayerAdminForm
    inlines = [MatchPlayerDetailInline]


# Register your models here.
admin.site.register(God)
admin.site.register(Item)
admin.site.register(Match)
admin.site.register(MatchPlayer, MatchPlayerAdmin)
admin.site.register(MatchPlayerDetail)
