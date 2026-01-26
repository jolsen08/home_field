from django.contrib import admin
from .models import Sport, Region, Season, AgeGroup, League, Registration


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'is_active']
    list_filter = ['state', 'is_active']
    search_fields = ['name', 'city', 'state']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'start_date', 'end_date', 'registration_open', 'registration_close']
    list_filter = ['name', 'year']
    ordering = ['-year', 'name']


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_age', 'max_age']
    ordering = ['min_age']


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport', 'region', 'season', 'age_group', 'status', 'spots_remaining']
    list_filter = ['status', 'sport', 'region', 'season', 'age_group']
    search_fields = ['name', 'description']
    raw_id_fields = ['coordinator']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'league', 'parent', 'status', 'registered_at']
    list_filter = ['status', 'league__sport', 'league__season']
    search_fields = ['student__first_name', 'student__last_name', 'parent__username']
    raw_id_fields = ['league', 'student', 'parent']
    date_hierarchy = 'registered_at'
