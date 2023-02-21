# properties.models

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField

from accounts.models import CustomUser


class Landlord(CustomUser):
    
    slug = AutoSlugField(populate_from='get_full_name', unique=True, unique_with='email', null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = _('Landlord')
        verbose_name_plural = _('Landlords')
        # abstract = True


class Properties(models.Model):

    prop_modes = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('to let', 'To Let')
    ]

    prop_types = [
        ('land', 'Land'),
        ('house', 'House'),
        ('office', 'Office space'),
        ('shop', 'Shop space'),
        ('apartment', 'Apartment')
    ]

    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=250)
    description = models.TextField()
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=prop_types, default='apartment')
    mode = models.CharField(max_length=50, choices=prop_modes, default='rent')
    size = models.PositiveIntegerField()
    bed = models.PositiveSmallIntegerField()
    bath = models.PositiveSmallIntegerField()
    toilet = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    slug = AutoSlugField(populate_from=f'get_title', unique=True, unique_with='landlord', null=True)

    def __str__(self):
        return f'{self.title}'

    def get_title(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')
        # abstract = True


class Inspection(models.Model):

    properties = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name='inspection')
    full_name = models.CharField(_("full_name"), max_length=50)
    phone_number = PhoneNumberField(region="NG")
    email = models.EmailField(_(""), max_length=254)
    date_and_time = models.DateTimeField(_(""), auto_now=False, auto_now_add=False)


class Tenant(CustomUser):
    
    # status_choices = [
    #     ('Tenant', 'Tenant'),
    #     ('Not tenant', 'Not tenant')
    # ]

    NG_states = [
        ('FC', 'Federal Capital Territory'),
        ('AB', 'Abia'),
        ('AD', 'Adamawa'),
        ('AK', 'Akwa Ibom'),
        ('AN', 'Anambra'),
        ('BA', 'Bauchi'),
        ('BY', 'Bayelsa'),
        ('BE', 'Benue'),
        ('BO', 'Borno'),
        ('CR', 'Cross River'),
        ('DE', 'Delta'),
        ('EB', 'Ebonyi'),
        ('ED', 'Edo'),
        ('EK', 'Ekiti'),
        ('EN', 'Enugu'),
        ('GO', 'Gombe'),
        ('IM', 'Imo'),
        ('JI', 'Jigawa'),
        ('KD', 'Kaduna'),
        ('KN', 'Kano'),
        ('KT', 'Katsina'),
        ('KE', 'Kebbi'),
        ('KO', 'Kogi'),
        ('KW', 'Kwara'),
        ('LA', 'Lagos'),
        ('NA', 'Nassarawa'),
        ('NI', 'Niger'),
        ('OG', 'Ogun'),
        ('ON', 'Ondo'),
        ('OS', 'Osun'),
        ('OY', 'Oyo'),
        ('PL', 'Plateau'),
        ('RI', 'Rivers'),
        ('SO', 'Sokoto'),
        ('TA', 'Taraba'),
        ('YO', 'Yobe'),
        ('ZA', 'Zamfara')
    ]

    relations = [
        ('family', 'Family'),
        ('friends', 'Friends'),
    ]

    spouse_relations = [
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorced', 'Divorced')
    ]

    properties = models.ForeignKey("properties.properties", verbose_name=_(""), on_delete=models.CASCADE, default='')
    current_address = models.TextField()
    place_of_employment = models.CharField(max_length=200)
    employment_address = models.TextField()
    position_or_grade_level = models.CharField(max_length=100)
    state_of_origin = models.CharField(choices=NG_states, max_length=15)
    religion = models.CharField(max_length=50, choices=[('CR','Christianity'), ('IS','Islam')])
    passport_photograph = models.ImageField(upload_to=f"images/pass_photo", height_field=None, width_field=None)
    no_of_occupants = models.PositiveSmallIntegerField()
    relationship_with_occupants = models.CharField(max_length=50, choices=relations, default='family')
    no_of_automobile = models.PositiveSmallIntegerField()
    current_landlord_name = models.CharField(max_length=100)
    reason_for_leaving = models.TextField()
    relationship = models.CharField(_("Relationship"), max_length=50, choices=spouse_relations)
    spouse = models.OneToOneField('properties.partner',  related_name='partner', on_delete=models.CASCADE)
    guarantor_1 = models.OneToOneField('properties.guarantor',  related_name='guarantor_1', on_delete=models.CASCADE, unique=True)
    guarantor_2 = models.OneToOneField('properties.guarantor',  related_name='guarantor_2', on_delete=models.CASCADE, unique=True)
    slug = AutoSlugField(populate_from=f'get_user', unique=True, null=False)
    # is_tenant = models.BooleanField(default=False)
    rent_start = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_user(self):
        return f'{self.username}'
    
    def approved_tenant(self):
        if self.is_tenant == True:
            self.is_tenant = False
        else:
            self.is_tenant = True
        self.save()

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')
        # abstract = True


class Partner(CustomUser):

    current_address = models.TextField()
    place_of_employment = models.CharField(max_length=200)
    religion = models.CharField(max_length=50, choices=[('CR','Christianity'), ('IS','Islam')])

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        # abstract = True


class Guarantor(CustomUser):
    
    passport_photograph = models.ImageField(upload_to=f"images/pass_photo", height_field=None, width_field=None)
    residential_address = models.TextField()
    place_of_employment = models.CharField(max_length=200)
    employment_address = models.TextField()

    class Meta:
        verbose_name = _('Guarantor')
        verbose_name_plural = _('Guarantors')
        # abstract = True


class OfficeTenant(CustomUser):
    pass


class Buyer(CustomUser):
    pass


class PropertiesIssues(models.Model):

    treat = [
        ('treated', 'Treated'),
        ('pending', 'Pending'),
        ('not-treated', 'Not Treated')
    ]
    
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name='issues')
    reported_by = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reporter')
    report = models.TextField()
    is_treated = models.CharField(choices=treat, max_length=20)

