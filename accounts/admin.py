from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'city', 'state']
    list_filter = ['role', 'state', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('HomeField Info', {'fields': ('role', 'phone', 'city', 'state', 'zip_code')}),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'parent', 'date_of_birth', 'gender', 'age']
    list_filter = ['gender', 'grade_level']
    search_fields = ['first_name', 'last_name', 'parent__username', 'parent__email']
    raw_id_fields = ['parent']
