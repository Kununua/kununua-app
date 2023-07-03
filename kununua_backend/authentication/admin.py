from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import KununuaUser, Address

class KununuaUserAdmin(UserAdmin):
    model = KununuaUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_picture']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile_picture',)
        })
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile_picture',)
        })
    )
    
admin.site.register(KununuaUser, KununuaUserAdmin)
admin.site.register(Address)