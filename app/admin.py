from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Test, User, UserProgress

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'phone_number', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'phone_number')
    ordering = ('username',)


admin.site.register(Test)
admin.site.register(UserProgress)