from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'registration_id', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('registration_id', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('registration_id', 'user_type')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)