from rest_framework import serializers
from mferp.auth.user.models import Account
from .models import BasicEmpInfo, PersonalEmpInfo, AccountEmpInfo, AddressEmpInfo


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
        fields = "__all__"
        


class BasicEmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicEmpInfo
        fields = "__all__"

class PersonalEmpSerializer(serializers.ModelSerializer):
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
