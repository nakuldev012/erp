from rest_framework import serializers
from mferp.upload.models import UploadedFile
from hr.hrconfig.models import HrConfig
from mferp.mastertableconfig.models import Organization
from mferp.auth.user.models import Account
from .models import (
    BasicEmpInfo,
    PersonalEmpInfo,
    AccountEmpInfo,
    AddressEmpInfo,
    PrimaryEmpInfo,
)
from rest_framework import serializers

# class MasterConfigSerializer( serializers.ModelSerializer,):
#     class Meta:
#         model = PrimaryEmpInfo
#         exclude = ('created_at', 'updated_at')

#     def validate(self, data):
#         if not data.get("label"):
#             raise exceptions.ValidationError('Measurement with this profile name already exists.')

#         if MasterConfig.objects.filter(label=data.get("label","")).exists():
#             raise ClientErrors("This label is already exists")

#         return super().validate(data)
#     def create(self, validated_data):
#         parent=validated_data.get("parent",None)

#         if parent is not None:
#             try:
#                 parent_category = MasterConfig.objects.get(id=parent.id)

#                 if parent_category.max_subcategory_level <= parent_category.children.count():
#                     raise serializers.ValidationError("Maximum subcategory level reached for the parent category.")
#                 validated_data['parent'] = parent_category  # Set the parent field
#             except MasterConfig.DoesNotExist:
#                 raise serializers.ValidationError("Parent category does not exist.")
#         else:
#             parent_category = None

#         # Create the new MasterConfig instance with the parent set
#         return super().create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "phone_number", "email"]


class BasicEmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicEmpInfo
        fields = "__all__"


# class UploadedFileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UploadedFile
#         fields = ('upload',)

#     def get_upload_url(self, obj):
#         return obj.upload if obj else None


class PersonalEmpSerializer(serializers.ModelSerializer):
    character_certificate = serializers.CharField(
        source="character_certificate.upload", read_only=True
    )
    medical_certificate = serializers.CharField(
        source="medical_certificate.upload", read_only=True
    )
    profile_pic = serializers.CharField(source="profile_pic.upload", read_only=True)

    class Meta:
        model = PersonalEmpInfo
        fields = "__all__"


    

class AccountEmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEmpInfo
        fields = "__all__"


class AddressEmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressEmpInfo
        fields = "__all__"


class PrimaryEmpInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    parent_org = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    child_org = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), many=True, allow_null=True
    )
    type_of_employment = serializers.PrimaryKeyRelatedField(
        queryset=HrConfig.objects.all()
    )
    category_of_employee = serializers.PrimaryKeyRelatedField(
        queryset=HrConfig.objects.all()
    )
    probation_end_date = serializers.DateTimeField(allow_null=True, required=False)
    designation = serializers.PrimaryKeyRelatedField(queryset=HrConfig.objects.all())
    cadre = serializers.PrimaryKeyRelatedField(queryset=HrConfig.objects.all())
    ladder = serializers.PrimaryKeyRelatedField(queryset=HrConfig.objects.all())
    shift = serializers.PrimaryKeyRelatedField(queryset=HrConfig.objects.all())
    isVerified = serializers.BooleanField(default=False)

    class Meta:
        model = PrimaryEmpInfo
        fields = "__all__"

    def child_representation(self, instance):
        data = super().to_representation(instance)
        data["child_org"] = [org.id for org in instance.child_org.all()]
        return data
