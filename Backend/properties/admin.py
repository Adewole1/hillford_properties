# properties.admin

from django.contrib import admin

from .models import Landlord, Properties, Tenant, Inspection, Guarantor, Partner


class GuarantorAdmin(admin.StackedInline):
    model = Guarantor
    

class PartnerAdmin(admin.TabularInline):
    model = Partner


class MyTenantAdmin(admin.ModelAdmin):
    	
	list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_tenant']
	fieldsets = (
		('Authentication', {'fields': ('email', 'password')}),
		('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_tenant', 
									   'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		('Custom info', {'fields': ('slug',)}),
	)
	readonly_fields = ('slug',)
	inlines = [
      PartnerAdmin,
      GuarantorAdmin
	]



admin.site.register(Landlord)
admin.site.register(Properties)
admin.site.register(Inspection)
admin.site.register(Tenant, MyTenantAdmin)