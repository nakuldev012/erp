from django.db import models
from mferp.common.validators import phone_validator
from mferp.address.models import BaseAddress
from mferp.upload.models import UploadedFile


class AbstractTime(models.Model):
    """For Every Database Table"""

    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    class Meta:
        abstract = True


class MasterConfig(AbstractTime):
    label = models.CharField(max_length=100)
    max_subcategory_level = models.PositiveIntegerField(default=5)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.label


class Organization(AbstractTime):
    """
    Create Organization on Database, Organization Model
    """

    type_of_organization = models.ForeignKey(
        "mastertableconfig.MasterConfig",
        on_delete=models.CASCADE,
        related_name="org_masterconfig_type",
    )
    ownership_status = models.ForeignKey(
        "mastertableconfig.MasterConfig",
        on_delete=models.CASCADE,
        related_name="org_masterconfig_ownership",
    )
    nature_of_organization = models.ForeignKey(
        "mastertableconfig.MasterConfig",
        on_delete=models.CASCADE,
        related_name="org_masterconfig_nature",
    )
    
    affiliated_university = models.ForeignKey(
        "mastertableconfig.MasterConfig",
        on_delete=models.CASCADE,
        related_name="org_masterconfig_aff_univ",null=True, blank=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    establishment_date = models.DateField()
    org_name = models.CharField(
        "Organization Name", max_length=250, null=False, blank=False
    )
    short_code = models.CharField(
        "Short Code",
        max_length=250,
        null=True,
        blank=True,
        unique=True,
    )
    
    logo_org = models.ImageField(upload_to="mferp/mastertableconfig/", max_length=250, null=True, blank=True)
    cover_banner_org = models.ImageField(upload_to="mferp/mastertableconfig/", max_length=250, null=True, blank=True)
    photo_org = models.ImageField(upload_to="mferp/mastertableconfig/", max_length=250, null=True, blank=True)
    # address = models.TextField("Address", null=True, blank=True)
    # city = models.CharField("City", max_length=150, null=True, blank=True)
    # landmark = models.CharField("Landmark", max_length=250, null=True, blank=True)
    # state = models.CharField("State", max_length=150,null=True, blank=True)
    # district = models.CharField(
    #     "District",
    #     max_length=250,null=True, blank=True
    # )
    # pin_code = models.CharField(
    #     "Pin Code",
    #     max_length=150,null=True, blank=True
    # )
    # email = models.EmailField(
    #     "Email Address",
    #     max_length=255,
    #     unique=True,null=True, blank=True
    # )
    # web_address = models.CharField("Web Address", max_length=255, null=True, blank=True)
    # contact_number = models.CharField(
    #     validators=[phone_validator], max_length=17, null=True, blank=True
    # )
    # phone_number = models.CharField(validators=[phone_validator], max_length=17,null=True, blank=True)
    # max_subcategory_level = models.PositiveIntegerField(default=5,null=True, blank=True)


class OrgAddress(BaseAddress):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="orgaddress_organization")
    region = models.ForeignKey(
        "mastertableconfig.MasterConfig",
        on_delete=models.CASCADE,
        related_name="orgaddress_region"
    )
    
    email = models.EmailField(
        "Email Address",
        max_length=255,
        unique=True
    )
    web_address = models.CharField("Web Address", max_length=255, null=True, blank=True)
    contact_number = models.CharField(
        validators=[phone_validator], max_length=17, null=True, blank=True
    )
    phone_number = models.CharField(validators=[phone_validator], max_length=17)


class Test(models.Model):
    name = models.CharField(max_length=100)
    cover_image = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name="test_uploadedfile",
        null=True,
        blank=True,
    )