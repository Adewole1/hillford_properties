# accounts/permissions.py

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    message = 'You do not have access'

    def has_permission(self, request, view):
        if view.action == 'list' and not request.user.is_superuser:
            return False
        
        if view.action == 'destroy' and not request.user.is_superuser:
            return False
        
        return request.method in ['POST'] or (request.user.is_authenticated and request.user.is_staff)
    #     if request.user.is_authenticated:
    #         return True
        
    #     if request.method == 'POST':
    #         return True
        
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     return False


    def has_object_permission(self, request, view, obj):
        
        if request.user.is_superuser:
            return True
        
        if view.action=='list' and not request.user.is_superuser:
            return False
        
        if view.action == 'destroy' and not request.user.is_superuser:
            return False

        return obj.email==request.user.email