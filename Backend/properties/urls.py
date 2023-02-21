# properties.urls

from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from django.views.generic.base import RedirectView


# router = SimpleRouter()

# router.register('tenants', views.TenantViewSet, basename='tenants')
# router.register('', views.PropertiesViewSet, basename='properties')
# router.register('landlord', views.LandlordViewSet, basename='landlords')

landlord_list = views.LandlordViewSet.as_view({
    'get': 'list'
})
landlord_details = views.LandlordViewSet.as_view({
    'get': 'retrieve'
})
landlord_create = views.LandlordViewSet.as_view({
    'post': 'create'
})
landlord_update = views.LandlordViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})
landlord_delete = views.LandlordViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

properties_list = views.PropertiesViewSet.as_view({
    'get': 'list'
})
properties_details = views.PropertiesViewSet.as_view({
    'get': 'retrieve'
})
properties_create = views.PropertiesViewSet.as_view({
    'post': 'create',
})
properties_update = views.PropertiesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})
properties_delete = views.PropertiesViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

inspection_list = views.PropertiesViewSet.as_view({
    'get': 'properties_inspection_list'
})
# inspection_details = views.PropertiesInspectionView.as_view({
#     'get': 'retrieve'
# })
inspection_create = views.PropertiesViewSet.as_view({
    'post': 'properties_inspection_new'
})
# inspection_update = views.PropertiesInspectionView.as_view({
#     'get': 'retrieve',
#     'put': 'update'
# })
# inspection_delete = views.PropertiesInspectionView.as_view({
#     'get': 'retrieve',
#     'delete': 'destroy'
# })

reports_list = views.PropertiesViewSet.as_view({
    'get': 'properties_issues_list'
})
# reports_details = views.PropertiesIssuesViewset.as_view({
#     'get': 'retrieve'
# })
reports_create = views.PropertiesViewSet.as_view({
    'post': 'properties_issues_new'
})
# reports_update = views.PropertiesIssuesViewset.as_view({
#     'get': 'retrieve',
#     'put': 'update'
# })
# reports_delete = views.PropertiesIssuesViewset.as_view({
#     'get': 'retrieve',
#     'delete': 'destroy'
# })

tenant_list = views.TenantViewSet.as_view({
    'get': 'list'
})
tenant_details = views.TenantViewSet.as_view({
    'get': 'retrieve'
})
tenant_create = views.TenantViewSet.as_view({
    'post': 'create'
})
tenant_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})
tenant_delete = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})
tenant_approval = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'approve_tenant'
})
tenant_password_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_password_update'
})
tenant_rent_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_rent_update'
})
tenant_passport_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_passport_update'
})
tenant_spouse_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_spouse_update'
})
tenant_g1_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_guarantor_1_update'
})
tenant_g2_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_guarantor_2_update'
})
tenant_g1_passport_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_guarantor_1_passport_update'
})
tenant_g2_passport_update = views.TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'tenant_guarantor_2_passport_update'
})


urlpatterns = [
    path("", RedirectView.as_view(pattern_name='properties-list', permanent=True), name="index"),
    path("properties/landlord/new", landlord_create, name="landlord-form"),
    path("properties/landlord/all", landlord_list, name="landlord-list"),
    path("properties/landlord/<slug:slug>", landlord_details, name="landlord-details"),
    path("properties/landlord/<slug:slug>/edit", landlord_update, name="landlord-update"),
    path("properties/landlord/<slug:slug>/delete", landlord_delete, name="landlord-delete"),
    path("properties/new", properties_create, name="properties-create"),
    path("properties/all", properties_list, name="properties-list"),
    path("properties/<slug:slug>", properties_details, name="properties-details"),
    path("properties/<slug:slug>/edit", properties_update, name="properties-update"),
    path("properties/<slug:slug>/delete", properties_delete, name="properties-delete"),
    path("properties/<slug:slug>/inspection/new", inspection_create, name="inspection-form"),
    path("properties/<slug:slug>/inspection/all", inspection_list, name="inspection-list"),
    # path("<slug:slug>/inspection/<int:pk>", inspection_details, name="inspection-details"),
    path("properties/<slug:slug>/reports/new", reports_create, name="inspection-form"),
    path("properties/<slug:slug>/reports/all", reports_list, name="inspection-list"),
    # path("<slug:slug>/reports/<int:pk>", inspection_details, name="inspection-details"),
    path("properties/<slug:slug>/tenants/new", tenant_create, name="tenant-create"),
    path("properties/<slug:slug>/tenants/all", tenant_list, name="tenant-list"),
    path("properties/tenants/<slug:slug>", tenant_details, name="tenant-details"),
    path("properties/tenants/<slug:slug>/edit", tenant_update, name="tenant-update"),
    path("properties/tenants/<slug:slug>/approve-tenant", tenant_approval, name="approve-tenant"),
    path("properties/tenants/<slug:slug>/password-edit", tenant_password_update, name="tenant-password-update"),
    path("properties/tenants/<slug:slug>/rent-edit", tenant_rent_update, name="tenant-rent-update"),
    path("properties/tenants/<slug:slug>/delete", tenant_delete, name="tenant-delete"),
    path("properties/tenants/<slug:slug>/passport-edit", tenant_passport_update, name="tenant-passport-update"),
    path("properties/tenants/<slug:slug>/spouse/edit", tenant_spouse_update, name="tenant-spouse-update"),
    path("properties/tenants/<slug:slug>/guarantor-1/edit", tenant_g1_update, name="tenant-guarantor1-update"),
    path("properties/tenants/<slug:slug>/guarantor-2/edit", tenant_g2_update, name="tenant-guarantor2-update"),
    path("properties/tenants/<slug:slug>/guarantor-1/passport-edit", tenant_g1_passport_update, name="tenant-passport-update"),
    path("properties/tenants/<slug:slug>/guarantor-2/passport-edit", tenant_g2_passport_update, name="tenant-passport-update"),
]
