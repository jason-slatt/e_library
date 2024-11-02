
from django.contrib import admin
from .models import UserRole, RoleChoices

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__email',)

admin.site.register(UserRole, UserRoleAdmin)


