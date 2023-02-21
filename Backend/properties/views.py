# properties.views

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions
from sms import send_sms

from authemail.models import PasswordResetCode

from .permissions import (AdminStaffOrReadOnly,
                          AllAdmin,
                          AllTenantAdmin,
                          CreateAdmin,
                          PermissionPolicyMixin)

from .serializers import (LandlordSerializer, 
                          PropertiesSerializers, 
                          PropertyInspectionSerializer, 
                          PropertiesIssuesSerializers,
                          TenantSerializer, 
                          TenantUpdateSerializer,
                          TenantPasswordUpdateSerializer,
                          TenantRentSerializer,
                          TenantSpouseUpdateSerializer,
                          TenantPassportUpdateSerializer,
                          TenantGuarantor1UpdateSerializer,
                          TenantGuarantor2UpdateSerializer,
                          TenantGuarantor1PassportUpdateSerializer,
                          TenantGuarantor2PassportUpdateSerializer)
from .models import Landlord, Properties, Inspection, Tenant, PropertiesIssues


class PropertiesViewSet(viewsets.ModelViewSet):

    serializer_class = PropertiesSerializers
    queryset = Properties.objects.all()
    lookup_field = 'slug'
    permission_classes = [AdminStaffOrReadOnly]
    filterset_fields = ['property_type', 'mode']
    search_fields = ['property_type', 'mode', 'title', ]
    ordering_fields = ['property_type', 'mode', 'bath', 'toilet', 'price']

    @action(detail=False, methods=['GET'], permission_classes=[CreateAdmin])
    def properties_inspection_list(self, request, *args, **kwargs):
        queryset = Inspection.objects.filter(properties=Properties.objects.get(slug=self.kwargs.get("slug")).id)
        serializer = PropertyInspectionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[CreateAdmin])
    def properties_inspection_new(self, request, *args, **kwargs):
        queryset = Inspection.objects.all()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer.save(properties=Properties.objects.get(slug=self.kwargs.get("slug")))
        to = serializer.data['email']
        name = serializer.data['full_name']
        phone = serializer.data['phone_number']
        props = Properties.objects.get(pk=serializer.data['properties'])
        address = props.address       

        date_time = serializer.data['date_and_time']

        body = f'There is an inspection review from {name} on {props} property at {address} by {date_time}. You can contact the person at {phone} and {to}'

        send_mail(subject='Property Inspection for {props} at {address}', 
                  message=body, 
                  recipient_list=[settings.DEFAULT_FROM_EMAIL],
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  fail_silently=False)

        # send_sms(
        #     body,
        #     'HillfordR',
        #     ['+2348038507100'],
        #     fail_silently=False
        # )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['GET'], permission_classes=[AllTenantAdmin])
    def properties_issues_list(self, request, *args, **kwargs):
        queryset = PropertiesIssues.objects.filter(properties=get_object_or_404(Properties, slug=self.kwargs.get("slug")).id)
        # queryset = Tenant.objects.filter(properties=Properties.objects.get(slug=self.kwargs.get("slug")).id)
        serializer = PropertiesIssuesSerializers(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[AllTenantAdmin])
    def properties_issues_new(self, request, *args, **kwargs):
        queryset = PropertiesIssues.objects.all()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(properties=Properties.objects.get(slug=self.kwargs.get("slug")), reported_by=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LandlordViewSet(viewsets.ModelViewSet):

    serializer_class = LandlordSerializer
    queryset = Landlord.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [AllTenantAdmin]
        else:
            permission_classes = [AllAdmin]
        return [permission() for permission in permission_classes]


# class PropertiesInspectionView(viewsets.ModelViewSet):

#     serializer_class = PropertyInspectionSerializer
#     queryset = Inspection.objects.all()
#     permission_classes = [CreateAdmin]

#     def list(self, request, *args, **kwargs):
#         queryset = Inspection.objects.filter(properties=Properties.objects.get(slug=self.kwargs.get("slug")).id)
#         serializer = PropertyInspectionSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def perform_create(self, serializer):
#         serializer.save(properties=Properties.objects.get(slug=self.kwargs.get("slug")))
#         to = serializer.data['email']
#         name = serializer.data['full_name']
#         phone = serializer.data['phone_number']
#         props = Properties.objects.get(pk=serializer.data['properties'])
#         address = props.address       

#         date_time = serializer.data['date_and_time']

#         body = f'There is an inspection review from {name} on {props} property at {address} by {date_time}. You can contact the person at {phone} and {to}'

#         # send_mail(subject='Property Inspection for {props} at {address}', 
#         #           message=body, 
#         #           recipient_list=[settings.DEFAULT_FROM_EMAIL],
#         #           from_email=settings.DEFAULT_FROM_EMAIL,
#         #             fail_silently=False)

#         # send_sms(
#         #     body,
#         #     'HillfordR',
#         #     ['+2348038507100'],
#         #     fail_silently=False
#         # )


# class PropertiesIssuesViewset(viewsets.ModelViewSet):
#     queryset = PropertiesIssues.objects.all()
#     serializer_class = PropertiesIssuesSerializers
#     # permission_classes = [AllTenantAdmin]

#     def list(self, request, *args, **kwargs):
#         queryset = PropertiesIssues.objects.filter(properties=get_object_or_404(Properties, slug=self.kwargs.get("slug")).id)
#         # queryset = Tenant.objects.filter(properties=Properties.objects.get(slug=self.kwargs.get("slug")).id)
#         serializer = PropertiesIssuesSerializers(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer(properties=Properties.objects.get(slug=self.kwargs.get("slug")), reported_by=request.user))
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
#     def get_permissions(self):
#         """
#         Instantiates and returns the list of permissions that this view requires.
#         """
#         if self.action == 'create' or self.action == 'list':
#             permission_classes = [AllTenantAdmin]
#         else:
#             permission_classes = [AllAdmin]
#         return [permission() for permission in permission_classes]


class TenantViewSet(viewsets.ModelViewSet):
    
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()
    lookup_field = 'slug'
    permission_classes = [CreateAdmin]

    def list(self, request, *args, **kwargs):
        queryset = Tenant.objects.filter(properties=get_object_or_404(Properties, slug=self.kwargs.get("slug")).id)
        # queryset = Tenant.objects.filter(properties=Properties.objects.get(slug=self.kwargs.get("slug")).id)
        serializer = TenantSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(properties=Properties.objects.get(slug=self.kwargs.get("slug")))
        # print(to, name, phone, props, date_time)

    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AllTenantAdmin])
    def update(self, request, *args, **kwargs):
        serializer = TenantUpdateSerializer
        queryset = Tenant.objects.all()
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=['PUT', 'GET'], permission_classes=[AllAdmin])
    def approve_tenant(self, request, *args, **kwargs):
        tenant = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        tenant.approved_tenant()
        if tenant.is_tenant:
            return Response({'Success':f'{tenant} is now a tenant'}, status=status.HTTP_202_ACCEPTED)
        return Response({'Success':f'{tenant} is no longer a tenant'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['PUT', 'GET'])
    def tenant_password_update(self, request, *args, **kwargs):
        # serializer = TenantPasswordUpdateSerializer(data=request.data)

        try:
            tenant = Tenant.objects.get(slug=kwargs.get('slug'))
            email = tenant.email
            # user = get_user_model().objects.get(email=tenant.email)

            # Delete all unused password reset codes
            PasswordResetCode.objects.filter(user=tenant).delete()
            if tenant.is_verified and tenant.is_active:
                password_reset_code = \
                    PasswordResetCode.objects.create_password_reset_code(tenant)
                password_reset_code.send_password_reset_email()
                content = {'email': email}
                return Response(content, status=status.HTTP_201_CREATED)
        except Tenant.DoesNotExist:
            pass

        content = {'detail': _('Password reset not allowed.')}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AllAdmin])
    def tenant_rent_update(self, request, *args, **kwargs):
        serializer = TenantRentSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if instance.is_tenant:
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST, 
                        context={'Error': 'User is not a tenant'})
    

    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_passport_update(self, request, *args, **kwargs):
        serializer = TenantPassportUpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_spouse_update(self, request, *args, **kwargs):
        serializer = TenantSpouseUpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_guarantor_1_update(self, request, *args, **kwargs):
        serializer = TenantGuarantor1UpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_guarantor_2_update(self, request, *args, **kwargs):
        serializer = TenantGuarantor2UpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_guarantor_1_passport_update(self, request, *args, **kwargs):
        serializer = TenantGuarantor1PassportUpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT', 'GET'], permission_classes=[AdminStaffOrReadOnly])
    def tenant_guarantor_2_passport_update(self, request, *args, **kwargs):
        serializer = TenantGuarantor2PassportUpdateSerializer
        queryset = get_object_or_404(Tenant, slug=kwargs.get("slug"))
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

# @api_view(['POST', 'GET'])
# @permission_classes([AllAdmin])
# def approve_tenant(request, *args, **kwargs):

#     tenant = get_object_or_404(Tenant, slug=kwargs.get("slug"))
#     tenant.approved_tenant()
#     if tenant.tenant == True:
#         return Response({'Success':f'{tenant} is now a tenant'})
#     return Response({'Success':f'{tenant} is no longer a tenant'})


# class TenantPasswordUpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantPasswordUpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()


# class TenantRentUdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantRentSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if serializer.data['is_tenant']:
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST, 
#                         context={'Error': 'User not a tenant'})


# class TenantUpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantUpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AllTenantAdmin]


# class TenantPassportUpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantPassportUpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]


# class TenantSpouseUpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantSpouseUpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', True)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)


# class TenantGuarantor1UpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantGuarantor1UpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', True)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)


# class TenantGuarantor2UpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantGuarantor2UpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', True)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)


# class TenantGuarantor1PassportUpdateViewset(viewsets.ModelViewSet):
#     serializer_class = TenantGuarantor1PassportUpdateSerializer
#     lookup_field = 'slug'
#     queryset = Tenant.objects.all()
#     permission_classes = [AdminStaffOrReadOnly]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', True)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)
    
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)


# class TenantGuarantor2PassportUpdateViewset(viewsets.ModelViewSet):
    # serializer_class = TenantGuarantor2PassportUpdateSerializer
    # lookup_field = 'slug'
    # queryset = Tenant.objects.all()
    # permission_classes = [AdminStaffOrReadOnly]

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', True)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)
    
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
