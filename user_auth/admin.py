from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Field yang ingin ditampilkan di halaman admin
    list_display = ('id', 'full_name', 'nip', 'email', 'roles', 'is_active', 'is_staff')
    
    # Field yang bisa dicari berdasarkan nama dan nip
    search_fields = ('full_name', 'nip')
    
    # Filter berdasarkan roles, aktif/non-aktif, dan staff
    list_filter = ('roles', 'is_active', 'is_staff')
    
    # Field untuk edit user
    fieldsets = (
        (None, {'fields': ('full_name', 'nip', 'email', 'password')}),
        ('Permissions', {'fields': ('roles', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Field untuk menambah user baru
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'nip', 'email', 'roles', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
