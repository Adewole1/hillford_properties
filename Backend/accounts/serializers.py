# accounts.serialilzers

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _ 
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField


from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from allauth.account import app_settings as allauth_account_settings

from .models import Staff


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


# class StaffRegisterSerializer(RegisterSerializer):

#     password1 = serializers.CharField(
#         write_only=True,
#         required=True,
#         label = 'Password',
#         # help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     password2 = serializers.CharField(
#         write_only=True,
#         required=True,
#         label = 'Password confirmation',
#         # help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password again'}
#     )

#     class Meta:
#         model = Staff
#         fields = ('first_name', 'last_name', 'phone_number', 'position', 'username', 'email', 'password', 'password2')


#     def validate_password1(self, value):
#         data = self.get_initial()
#         password = data.get('password2')
#         password2 = value
#         if password != password2:
#             raise ValidationError('Passwords must match')
#         return make_password(value)

#     def validate_password2(self, value):
#         data = self.get_initial()
#         password = data.get('password1')
#         password2 = value
#         if password != password2:
#             raise ValidationError('Passwords must match')
#         return make_password(value)
    
#     def get_cleaned_data(self):
#         return {
#         'username': self.validated_data.get('username', ''),
#         'first_name': self.validated_data.get('first_name', ''),
#         'last_name': self.validated_data.get('last_name', ''),
#         'position': self.validated_data.get('username', ''),
#         'phone_number': self.validated_data.get('phone_number', ''),
#         'password1': self.validated_data.get('password1', ''),
#         'password2': self.validated_data.get('password2', ''),
#         'email': self.validated_data.get('email', ''),
#     }


#     def custom_signup(self, request, user):
#         self.cleaned_data = self.get_cleaned_data()
#         my_group = get_object_or_404(Group, name='Hillford Staff')
#         self.cleaned_data.pop('password2')
#         if self.cleaned_data.get('position')=='CEO':
#             user = Staff.objects.create(**self.cleaned_data, is_staff=True, is_superuser=True, is_active=True)
#         else:
#             user = Staff.objects.create(**self.cleaned_data, is_staff=True, is_active=True)
#         user.set_password(self.cleaned_data['password'])
#         my_group.user_set.add(user)
#         user.save()

class StaffSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        label = 'Password',
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    re_password = serializers.CharField(
        write_only=True,
        required=True,
        label = 'Password confirmation',
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password again'}
    )

    class Meta:
        model = Staff
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'position', 'email', 'password', 're_password')


    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('re_password')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        return make_password(value)

    def validate_re_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        return make_password(value)
    
    # def validate_email(self, email):
    #     data = self.get_initial()
    #     # email = data.get('password')
    #     email = get_adapter().clean_email(email)
        
    #     if allauth_account_settings.UNIQUE_EMAIL:
    #         if email and email_address_exists(email):
    #             raise serializers.ValidationError(
    #                 _('A user is already registered with this e-mail address.'),
    #             )
    #     return email
    
    # def get_cleaned_data(self):
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', ''),
    #         'position': self.validated_data.get('position', ''),
    #         'phone_number': self.validated_data.get('phone_number', ''),
    #         'password': self.validated_data.get('password', ''),
    #         'email': self.validated_data.get('email', '')
    #     }

    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     # print(user)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self)
    #     # self.custom_signup(request, user)
    #     setup_user_email(request, user, [])
    #     return user
    
    # def create(self, validated_data):
    #     my_group = get_object_or_404(Group, name='Hillford Staff')
    #     validated_data.pop('re_password')
        
    #     if validated_data.get('position')=='CEO':
    #         user = Staff.objects.create(**validated_data, is_staff=True, is_superuser=True, is_active=False)
    #     else:
    #         user = Staff.objects.create(**validated_data, is_staff=True, is_active=False)
            
    #     user.set_password(validated_data['password'])
    #     my_group.user_set.add(user)
    #     return user

