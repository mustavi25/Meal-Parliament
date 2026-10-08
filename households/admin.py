from django.contrib import admin
from .models import Household, HouseholdMember

class HouseholdMemberInline(admin.TabularInline):
    model = HouseholdMember
    extra = 1
    autocomplete_fields = ['user']

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'invite_code', 'created_at', 'member_names')
    search_fields = ('name', 'invite_code')
    list_filter = ('created_at', 'members__user')
    inlines = [HouseholdMemberInline]

    def member_names(self, obj):
        members = obj.members.select_related('user').all()
        return ", ".join(m.user.username for m in members) or "—"
    member_names.short_description = "Members"

@admin.register(HouseholdMember)
class HouseholdMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'household', 'role', 'joined_at')
    search_fields = ('user__username', 'household__name')
    list_filter = ('role', 'joined_at')