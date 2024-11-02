# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from user_auth.models import UserRole, RoleChoices

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1
    can_delete = False

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'is_active', 'is_staff',)
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    
    inlines = [UserRoleInline]  # Allows role management directly within User admin

admin.site.register(User, UserAdmin)
