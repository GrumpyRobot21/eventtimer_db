from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'name', 'is_staff')
    search_fields = ('username', 'email', 'name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('eventCategory', 'details', 'duration', 'user', 'created_at')
    list_filter = ('eventCategory', 'user', 'created_at')
    search_fields = ('eventCategory', 'details', 'user__username')
    ordering = ('-created_at',)
