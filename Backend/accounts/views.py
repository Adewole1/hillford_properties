# accounts.views

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenVerifyView

# from dj_rest_auth.registration.views import RegisterView

# from authemail import wrapper
from authemail.views import Signup
from authemail.models import SignupCode
from authemail.models import send_multi_format_email
# from djoser.views import UserViewSet
# from djoser import signals

from .serializers import StaffSerializer, MyTokenObtainPairSerializer
from .models import Staff
from .permissions import IsAdminOrReadOnly


class StaffCreateView(Signup):

    serializer_class = StaffSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)
    #     data = self.get_response_data(user)

    #     if data:
    #         pos = serializer.data['position']
    #         user.is_staff = True
    #         if pos=='CEO':
    #             user.is_superuser = True
    #         my_group = get_object_or_404(Group, name='Hillford Staff')
    #         my_group.user_set.add(user)

    #         if pos=='CEO':
    #             user.is_superuser = True
            
    #         response = Response(
    #             data,
    #             status=status.HTTP_201_CREATED,
    #             headers=headers,
    #         )
    #     else:
    #         response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

    #     return response

    def post(self, request, format=None):
        serializer = StaffSerializer(data=request.data)

        if serializer.is_valid():
            print(request.data)
            email = serializer.data['email']
            password = request.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            pos = serializer.data['position']

            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

            try:
                user = Staff.objects.get(email=email)
                if user.is_verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Delete old signup codes
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except Staff.DoesNotExist:
                if pos=='CEO':
                    user = Staff.objects.create(email=email, is_staff=True, is_superuser=True, is_active=True)
                else:
                    user = Staff.objects.create(email=email, is_staff=True, is_active=True)
                # user2 = get_user_model().objects.create_user(email=email, first_name=first_name, last_name=last_name)

            # Set user fields provided
            user.set_password(password)
            # user2.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            my_group = get_object_or_404(Group, name='Hillford Staff')
            my_group.user_set.add(user)
            if not must_validate_email:
                user.is_verified = True
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
            user.save()

            if must_validate_email:
                # Create and associate signup code
                ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
                signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
                signup_code.send_signup_email()

            content = {'email': email, 'first_name': first_name,
                       'last_name': last_name}
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffViewSet(viewsets.ModelViewSet):

    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return StaffSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # clas = Signup()
    #     # response = clas.post(request=request)
    #     # return response


    #     # first_name=str(serializer.validated_data['first_name'])
    #     # last_name=str(serializer.validated_data['last_name'])
    #     # email=str(serializer.validated_data['email'])
    #     # password=serializer.validated_data['password']

    #     # print(first_name, last_name, email, password)

    #     # account = wrapper.Authemail()
    #     # response = account.signup(first_name=first_name, last_name=last_name, email=email, password=password)
    #     # response = account.signup(serializer.validated_data)
    #     self.perform_create(serializer)

    #     # user = Staff.objects.get(email=serializer.validated_data['email'])
    #     # current_site = get_current_site(request)
    #     # subject = 'Activate Your MySite Account'
    #     # token = MyTokenObtainPairSerializer()
    #     # message = render_to_string('accounts/email_confirmation.html', {
    #     #         'user': user,
    #     #         'domain': current_site.domain,
    #     #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     #         'token': token.get_token(user),
    #     #     })
    #     # # user.email_user(subject, message)
    #     # email = EmailMessage(
    #     #     subject,
    #     #     message,
    #     #     settings.EMAIL_HOST_USER,
    #     #     [user.email]
    #     # )
    #     # email.fail_silently = False
    #     # email.send()

    #     headers = self.get_success_headers(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # @action(detail=False, methods=['POST'])
    # def activation(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # user = serializer.user
    #     # user.is_active = True
    #     # user.save()
    #     try:
    #         # uid = force_str(urlsafe_base64_decode(uidb64))
    #         # user = Staff.objects.get(pk=uid)
    #         user = serializer.get_user()
    #     except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
    #         user = None


    #     signals.user_activated.send(
    #         sender=self.__class__, user=user, request=self.request
    #     )
    #     print(user)

    #     if user is not None:
    #         user.is_active = True
    #         # user.profile.email_confirmed = True
    #         user.save()
    #         # login(request, user)
    #         # message = {'Your account have been confirmed.'))
    #         return Response({'Success':f'Your account has been confirmed'}, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         return Response({'Success':f'The confirmation link was invalid, possibly because it has already been used.'}, 
    #                         status=status.HTTP_400_BAD_REQUEST)
    #         # messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
    #         # return redirect('home')

# class StaffRegisterViewSet(viewsets.ModelViewSet):
    
#     serializer_class = StaffRegisterSerializer
#     queryset = Staff.objects.all()
#     lookup_field = 'slug'
#     permission_classes = [IsAdminOrReadOnly]



