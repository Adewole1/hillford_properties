# accounts.urls

from django.urls import path
from rest_framework.routers import SimpleRouter



from . import views

admin_list = views.StaffViewSet.as_view({
    'get': 'list'
})
admin_details = views.StaffViewSet.as_view({
    'get': 'retrieve'
})
# admin_create = views.StaffViewSet.as_view({
#     'post': 'create'
# })
admin_update = views.StaffViewSet.as_view({
    'put': 'update',
    'get': 'retrieve'
})
admin_delete = views.StaffViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})
# admin_activate = views.StaffViewSet.as_view({
#     'get': 'retrieve',
#     'post': 'activate'
# })


urlpatterns = [
    # path("staff/new", admin_create, name="staff-create"),
    path("staff/new", views.StaffCreateView.as_view(), name="staff-create"),
    path("staff/all", admin_list, name="staff-list"),
    path("staff/<slug:slug>", admin_details, name="staff-details"),
    path("staff/<slug:slug>/edit", admin_update, name="staff-update"),
    path("staff/<slug:slug>/delete", admin_delete, name="staff-delete"),
    # path('activate/<uidb64>/<token>/', admin_activate, name='staff-activate'),
]