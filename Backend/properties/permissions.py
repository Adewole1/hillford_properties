# properties.permissions

from rest_framework import permissions

class PermissionPolicyMixin:

    def check_permissions(self, request):

        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler and self.permission_classes_per_method 
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permision_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)
    

class AdminStaffOrReadOnly(permissions.BasePermission):

    message = 'You do not have access'
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action == 'destroy' and not request.user.is_superuser:
                return False

            return True
        
        else:
            if request.method in permissions.SAFE_METHODS:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True

        if view.action == 'destroy' and not request.user.is_superuser:
            return False

        return False
    

class AllAdmin(permissions.BasePermission):

    message = 'You do not have access'

    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_superuser:
            return True
        
        if request.user.is_staff:
            return True
        
        return False
    

class AllTenantAdmin(permissions.BasePermission):

    message = 'You do not have access'
    
    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_superuser:
            return True
        
        if request.user.is_staff:
            return True
        
        if request.user.is_tenant:
            return True
        
        return False


class CreateAdmin(permissions.BasePermission):

    message = 'You do not have access'
    
    def has_permission(self, request, view):
        print(request.method)
        # print(view.action == 'create' or request.user and request.user.is_authenticated)
        return request.method=='POST' or request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print(view.action)
        return (request.user.is_staff) or (request.user.is_superuser) or (request.user.is_tenant)