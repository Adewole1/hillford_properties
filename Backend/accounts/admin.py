from django.contrib import admin
from django.contrib.auth import get_user_model

from authemail.admin import EmailUserAdmin

from .models import Staff, CustomUser


class MyUserAdmin(EmailUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_tenant']
    fieldsets = (
		('Authentication', {'fields': ('email', 'password')}),
		('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_tenant', 
									   'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		# ('Custom info', {'fields': ('slug',)}),
	)


class MyStaffAdmin(admin.ModelAdmin):
    	
	list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
	fieldsets = (
		('Authentication', {'fields': ('email', 'password')}),
		('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_tenant', 
									   'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		('Custom info', {'fields': ('slug',)}),
	)
	readonly_fields = ('slug',)
        



admin.site.unregister(get_user_model())
admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Staff, MyStaffAdmin)