from mferp.auth.user.models import Account
from django.db import models
from mferp.mastertableconfig.models import MasterConfig, AbstractTime, Organization
from hr.hrconfig.models import HrConfig
from mferp.common.validators import phone_validator
from django.core.validators import MinLengthValidator
from mferp.address.models import BaseAddress, City
from mferp.upload.models import UploadedFile


class PrimaryEmpInfo(AbstractTime):
    user_id = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="primempinfo_account"
    )
    parent_org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="primempinfo_org", null=True, blank=True
    )
    child_org = models.ManyToManyField(
        Organization, related_name="primempinfo_child_org", null=True, blank=True
    )
    type_of_employment = models.ForeignKey(
        HrConfig, on_delete=models.CASCADE, related_name="primempinfo_hrconfig_emp_type", null=True, blank=True
    )
    probation_end_date = models.DateTimeField(null=True, blank=True)
    category_of_employee = models.ForeignKey(
        HrConfig,
        on_delete=models.CASCADE,
        related_name="primempinfo_hrconfig_emp_category",null=True, blank=True
    )
    designation = models.ForeignKey(
        HrConfig,
        on_delete=models.CASCADE,
        related_name="primempinfo_hrconfig_designation",null=True, blank=True
    )
    cadre = models.ForeignKey(
        HrConfig, on_delete=models.CASCADE, related_name="primempinfo_hrconfig_cadre", null=True, blank=True
    )
    ladder = models.ForeignKey(
        HrConfig, on_delete=models.CASCADE, related_name="primempinfo_hrconfig_ladder", null=True, blank=True
    )
    shift = models.ForeignKey(
        HrConfig, on_delete=models.CASCADE, related_name="primempinfo_hrconfig_shift", null=True, blank=True
    )
    isVerified = models.BooleanField(
        "Verified", default=False
    )

    # def __str__(self):
    #     return self.user_id.email


class BasicEmpInfo(AbstractTime):
    emp_id = models.OneToOneField(
        PrimaryEmpInfo,
        on_delete=models.CASCADE,
        related_name="basicempinfo_primempinfo",
    )
    emp_code = models.CharField(
        "Employee ID", max_length=100, null=True, blank=True, unique=True
    )
    title = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="basicempinfo_title"
    )
    department = models.ManyToManyField(
        MasterConfig, related_name="basicempinfo_department"
    )
    dob = models.DateTimeField()
    doj = models.DateTimeField(auto_now_add=True)
    additional_responsibility = models.ManyToManyField(
        HrConfig,
        related_name="basicempinfo_hrconfig",
        null=True,
        blank=True,
    )
    isVerified = models.BooleanField(
        "Verified", default=False
    )

    def __str__(self):
        return self.emp_id.user_id.email


class PersonalEmpInfo(AbstractTime):
    emp_id = models.OneToOneField(
        PrimaryEmpInfo,
        on_delete=models.CASCADE,
        related_name="personalempinfo_primempinfo",
    )
    father_name = models.CharField(max_length=30, blank=True, null=True)
    mother_name = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="personalempinfo_upload"
    )
    blood_group = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_bloodgroup",
    )
    gender = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_gender",
    )
    nationality = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_nationality",
    )
    caste = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_caste",
    )
    marital_status = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_marital_status",
    )
    religion = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_religion",
    )
    alternative_email = models.EmailField(
        "Alternative Email Address", null=True, blank=True, unique=True
    )
    office_email = models.EmailField(
        "Official Email Address", null=True, blank=True, unique=True
    )
    alternative_mobile_number = models.CharField(
        validators=[phone_validator], blank=True, null=True, unique=True, max_length=15
    )
    emergency_contact_name = models.CharField(max_length=250)
    emergency_contact_mobile_number = models.CharField(validators=[phone_validator], max_length=15)
    relationship = models.ForeignKey(
        MasterConfig,
        on_delete=models.CASCADE,
        related_name="personalempinfo_masterconfig_relationship",
    )
    son_count = models.IntegerField(blank=True, null=True)
    daughter_count = models.IntegerField(blank=True, null=True)
    isVerified = models.BooleanField(
        "Verified", default=False
    )
    character_certificate = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="personalempinfo_uploadfile_character_certificate"
    )
    medical_certificate = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="personalempinfo_uploadfile_medical_certificate"
    )

    def __str__(self):
        return self.emp_id.user_id.email


class AccountEmpInfo(AbstractTime):
    emp_id = models.OneToOneField(PrimaryEmpInfo, on_delete=models.PROTECT, related_name="accountempinfo_primempinfo")
    bank_name = models.CharField(max_length=500, null=True, blank=True)
    aadhar_no = models.CharField(max_length=12,validators=[MinLengthValidator(10)], unique=True)
    pan_no = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(10)])
    bank_account_no = models.CharField(max_length=25, unique=True, null=True, blank=True)
    uan_no = models.CharField(max_length=12, unique=True, validators=[MinLengthValidator(12)], null=True, blank=True)
    pf_no = models.CharField(max_length=30, unique=True, null=True, blank=True)
    bank_ifsc_code = models.CharField(
        max_length=11, validators=[MinLengthValidator(11)], null=True, blank=True
    )
    esic_no = models.CharField(max_length=17, unique=True, validators=[MinLengthValidator(17)])
    isVerified = models.BooleanField(
        "Verified", default=False
    )

    def __str__(self):
        return self.employee.user.email


class AddressEmpInfo(BaseAddress):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="addressempinfo_primempinfo")
    address_proof = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="addressempinfo_uploadfile"
    )
    isVerified = models.BooleanField(
        "Verified", default=False
    )
    is_both_address_same = models.BooleanField(
        "Is Both Address Same", default=False
    )

    def __str__(self):
        return self.type


class AcademicEmpInfo(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="academicempinfo_primempinfo")
    board_or_university = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="academicempinfo_masterconfig_boardoruniversity"
    )
    qualification_type = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="academicempinfo_masterconfig_qualification_type"
    )
    institute_name = models.CharField(max_length=250)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="academicempinfo_city", null=True, blank=True,
    )
    passing_year = models.DateTimeField()
    issue_date = models.DateTimeField("issue date", null=True, blank=True,)
    award_date = models.DateTimeField("award date", null=True, blank=True,)
    percentage = models.CharField(max_length=5)
    mark_sheet = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="academicempinfo_uploadfile_marksheet"
    )
    passing_certificate = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="academicempinfo_uploadfile_passingcertificate"
    )
    is_highest_qualification = models.BooleanField(
        default=False
    )
    
    is_verified = models.BooleanField(
        "Verified", default=False
    )

    def __str__(self):
        self.qualification_type






class CertificationEmpInfo(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="certificationempinfo_primempinfo")
    organization_name = models.CharField(max_length=250)
    completion_year = models.DateTimeField()
    specialization_area = models.CharField(max_length=500)
    is_verified = models.BooleanField(
        "Verified", default=False
    )
    is_highest_qualification = models.BooleanField(
        "highest qualification", default=False
    )
    completion_certificate = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="certificate_upload"
    )

    def __str__(self):
        return self.specialization_area


class DoctorateEmpInfo(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="doctorate_primempinfo")
    phd_status = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="doctorate_masterconfig_phdstatus"
    )
    university = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="doctorate_masterconfig_university"
    )
    research_topic = models.CharField(max_length=500)
    specialization_area = models.CharField(max_length=500)
    registration_date = models.DateTimeField("registration date")
    issue_date = models.DateTimeField("issue date", null=True, blank=True,)
    award_date = models.DateTimeField("award date", null=True, blank=True,)
    degree = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="doctorate_upload_degree", null=True, blank=True,
    )
    is_verified = models.BooleanField(
        "Verified", default=False
    )
    is_highest_qualification = models.BooleanField(
        "highest qualification", default=False
    )

    def __str__(self):
        return self.degree


class EmpPreviousExp(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="prev_exp_primempinfo")
    experience_type = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="expierence_master_exp_type"
    )
    from_date = models.DateTimeField("from date")
    to_date = models.DateTimeField("to date")
    effective_experience = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    designation = models.CharField(max_length=250, null=True, blank=True,)
    agp = models.CharField(max_length=100, null=True, blank=True,)
    gross_slary = models.CharField(max_length=100, null=True, blank=True,)
    remarks = models.TextField(null=True, blank=True)
    experience_letter = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="prevexp_upload_exp_letter", null=True, blank=True,
    )
    relieving_letter = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="prevexp_upload_relieving_letter", null=True, blank=True,
    )
    is_verified = models.BooleanField(
        "Verified", default=False
    )

    def __str__(self):
        return self.experience_type


class EmpCurrentExp(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="current_exp_primempinfo")
    experience_type = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="prevexp_master_exp_type"
    )
    from_date = models.DateTimeField("from date")
    to_date = models.DateTimeField("to date")
    effective_experience = models.CharField(max_length=100)
    agp = models.CharField(max_length=50, null=True, blank=True)
    designation = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="emp_designation", null=True, blank=True
    )
    gross_slary = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    total_effective_experience = models.CharField(max_length=100)
    
    is_verified = models.BooleanField(
        "Verified", default=False
    )

    def __str__(self):
        return self.experience_type


class EmpReporting(AbstractTime):
    employee = models.ForeignKey(PrimaryEmpInfo, on_delete=models.CASCADE, related_name="reporting_primempinfo" ,null=True, blank=True)
    reporting_type = models.ForeignKey(
        MasterConfig, on_delete=models.CASCADE, related_name="emp_reporting_type", null=True, blank=True
    )
    level = models.IntegerField(null=True, blank=True)
    reporting_to = models.ManyToManyField(PrimaryEmpInfo, related_name="reporting_to_primempinfo" ,null=True, blank=True)
    is_verified = models.BooleanField(
        "Verified", default=False, null=False, blank=False
    )

    def __str__(self):
        return self.reporting_type
