from rest_framework import serializers, validators
from rest_framework.fields import empty
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Properties, Landlord, Inspection, Tenant, Partner, Guarantor, PropertiesIssues

class PropertiesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Properties
        fields = "__all__"


class PropertiesIssuesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = PropertiesIssues
        fields = "__all__"
        read_only_fields = ['properties', 'reported_by', 'is_treated']


class LandlordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Landlord
        fields = ('first_name', 'last_name', 'email', 'phone_number')



class PropertyInspectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inspection
        fields = "__all__"
        read_only_fields = ['properties']


class PartnerSerializer(serializers.ModelSerializer):

    # email = serializers.EmailField(validators=[])
    
    class Meta:
        model = Partner
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'current_address', 'place_of_employment', 'religion')

class PartnerUpdateSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(validators=[])
    
    class Meta:
        model = Partner
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'current_address', 'place_of_employment', 'religion')


class GuarantorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Guarantor
        fields = ('passport_photograph', 'first_name', 'last_name', 'email', 'phone_number', 'residential_address', 'place_of_employment', 'employment_address')


class GuarantorPassportUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Guarantor
        fields = ('passport_photograph', 'first_name', 'last_name', 'email', 'phone_number', 'residential_address', 'place_of_employment', 'employment_address')
        read_only_fields = ('first_name', 'last_name', 'email', 'phone_number', 'residential_address', 'place_of_employment', 'employment_address')


class GuarantorDataUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Guarantor
        fields = ('passport_photograph', 'first_name', 'last_name', 'email', 'phone_number', 'residential_address', 'place_of_employment', 'employment_address')
        read_only_fields = ('passport_photograph',)


class TenantSerializer(serializers.ModelSerializer):

    spouse = PartnerSerializer()
    guarantor_1 = GuarantorSerializer()
    guarantor_2 = GuarantorSerializer()

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'rent_start', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['properties', 'slug', 'is_tenant', 'rent_start']

    def create(self, validated_data):
        sp = validated_data.pop('spouse')
        g1 = validated_data.pop('guarantor_1')
        g2 = validated_data.pop('guarantor_2')
        spouse_data = Partner.objects.create(**sp)
        gua1_data = Guarantor.objects.create(**g1)
        gua2_data = Guarantor.objects.create(**g2)
        tenant = Tenant.objects.create(**validated_data, spouse=spouse_data, guarantor_1=gua1_data, guarantor_2=gua2_data)
        return tenant


class TenantRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['rent_start']
        read_only_fields = ['properties', 'first_name', 'last_name', 'is_tenant']


class TenantPasswordUpdateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'password']

    # def update(self, instance, validated_data):

    #     return super().update(instance, validated_data)


class TenantUpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    # guarantor_1 = GuarantorSerializer()
    # guarantor_2 = GuarantorSerializer()

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['properties', 'slug', 'is_tenant', 'passport_photograph', 'spouse', 'guarantor_1', 'guarantor_2']


class TenantPassportUpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    # guarantor_1 = GuarantorSerializer()
    # guarantor_2 = GuarantorSerializer()

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['is_tenant', 'slug', 'properties', 'first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']


class TenantSpouseUpdateSerializer(serializers.ModelSerializer):
    
    spouse = PartnerSerializer()
    # guarantor_1 = GuarantorSerializer()
    # guarantor_2 = GuarantorSerializer()

    def __init__(self, instance, data=empty, **kwargs):
        
        if (
            data is not empty and
            'spouse.email' in data and
            instance.spouse is not None and
            instance.spouse.email == data['spouse.email']
        ):
            _mutable = data._mutable
            # set to mutable
            data._mutable = True
            data.pop('spouse.email')
            # set mutable flag back
            data._mutable = _mutable
        super(TenantSpouseUpdateSerializer, self).__init__(instance, data=data, **kwargs)


    def update(self, instance, validated_data):
        if 'spouse' in validated_data:
            nested_serializer = self.fields['spouse']
            nested_instance = instance.spouse
            nested_data = validated_data.pop('spouse')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(TenantSpouseUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']

        read_only_fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'guarantor_1', 'guarantor_2']


class TenantGuarantor1UpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    guarantor_1 = GuarantorDataUpdateSerializer()
    # guarantor_2 = GuarantorSerializer()

    def __init__(self, instance, data=empty, **kwargs):
        
        if (
            data is not empty and
            'guarantor_1.email' in data and
            instance.guarantor_1 is not None and
            instance.guarantor_1.email == data['guarantor_1.email']
        ):
            _mutable = data._mutable
            # set to mutable
            data._mutable = True
            data.pop('guarantor_1.email')
            # set mutable flag back
            data._mutable = _mutable
        super(TenantGuarantor1UpdateSerializer, self).__init__(instance, data=data, **kwargs)

    def update(self, instance, validated_data):
        if 'guarantor_1' in validated_data:
            nested_serializer = self.fields['guarantor_1']
            nested_instance = instance.guarantor_1
            nested_data = validated_data.pop('guarantor_1')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(TenantGuarantor1UpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 
                  'email', 'phone_number', 'current_address', 'place_of_employment', 'employment_address', 
                  'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 
                  'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name', 
                  'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2',]
        
        read_only_fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 
                            'email', 'phone_number', 'current_address', 'place_of_employment', 
                            'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 
                            'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 
                            'current_landlord_name', 'reason_for_leaving', 'relationship', 'spouse', 'guarantor_2']


class TenantGuarantor2UpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    # guarantor_1 = GuarantorSerializer()
    guarantor_2 = GuarantorDataUpdateSerializer()

    def __init__(self, instance, data=empty, **kwargs):
        
        if (
            data is not empty and
            'guarantor_2.email' in data and
            instance.guarantor_2 is not None and
            instance.guarantor_2.email == data['guarantor_2.email']
        ):
            _mutable = data._mutable
            # set to mutable
            data._mutable = True
            data.pop('guarantor_2.email')
            # set mutable flag back
            data._mutable = _mutable
        super(TenantGuarantor2UpdateSerializer, self).__init__(instance, data=data, **kwargs)

    def update(self, instance, validated_data):
        if 'guarantor_2' in validated_data:
            nested_serializer = self.fields['guarantor_2']
            nested_instance = instance.guarantor_2
            nested_data = validated_data.pop('guarantor_2')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(TenantGuarantor2UpdateSerializer, self).update(instance, validated_data)
    

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1']


class TenantGuarantor1PassportUpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    guarantor_1 = GuarantorPassportUpdateSerializer()
    # guarantor_2 = GuarantorSerializer()

    def update(self, instance, validated_data):
        if 'guarantor_1' in validated_data:
            nested_serializer = self.fields['guarantor_1']
            nested_instance = instance.guarantor_1
            nested_data = validated_data.pop('guarantor_1')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(TenantGuarantor1PassportUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_2']


class TenantGuarantor2PassportUpdateSerializer(serializers.ModelSerializer):
    
    # spouse = PartnerSerializer()
    # guarantor_1 = GuarantorSerializer()
    guarantor_2 = GuarantorPassportUpdateSerializer()

    def update(self, instance, validated_data):
        if 'guarantor_2' in validated_data:
            nested_serializer = self.fields['guarantor_2']
            nested_instance = instance.guarantor_2
            nested_data = validated_data.pop('guarantor_2')

            # Runs the update on whatever serializer the nested data belongs to
            nested_serializer.update(nested_instance, nested_data)

        # Runs the original parent update(), since the nested fields were
        # "popped" out of the data
        return super(TenantGuarantor2PassportUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = Tenant
        # exclude = ['password']
        fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1', 'guarantor_2']
        read_only_fields = ['is_tenant', 'slug', 'properties', 'passport_photograph','first_name', 'last_name', 'email', 'phone_number', 'current_address',
        'place_of_employment', 'employment_address', 'position_or_grade_level', 'state_of_origin', 'religion', 'no_of_occupants', 'relationship_with_occupants', 'no_of_automobile', 'current_landlord_name',
        'reason_for_leaving', 'relationship', 'spouse', 'guarantor_1']