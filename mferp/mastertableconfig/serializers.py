from rest_framework import serializers
from .models import MasterConfig, Organization, OrgAddress, Test
from rest_framework import status, response, exceptions, views
from mferp.common.errors import ClientErrors


class MasterConfigSerializer( serializers.ModelSerializer,):
    class Meta:
        model = MasterConfig
        exclude = ('created_at', 'updated_at')

    def validate(self, data):
        if not data.get("label"):
            raise exceptions.ValidationError('Measurement with this profile name already exists.')
		
        if MasterConfig.objects.filter(label=data.get("label","")).exists():
            raise ClientErrors("This label is already exists")

        return super().validate(data)
    def create(self, validated_data):
        parent=validated_data.get("parent",None)
        
        if parent is not None:
            try:
                parent_category = MasterConfig.objects.get(id=parent.id)

                if parent_category.max_subcategory_level <= parent_category.children.count():
                    raise serializers.ValidationError("Maximum subcategory level reached for the parent category.")
                validated_data['parent'] = parent_category  # Set the parent field
            except MasterConfig.DoesNotExist:
                raise serializers.ValidationError("Parent category does not exist.")
        else:
            parent_category = None
       
        # Create the new MasterConfig instance with the parent set
        return super().create(validated_data)
    

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('created_at', 'updated_at')  

    def create(self, validated_data):
       
        parent=validated_data.get("parent",None)
        
        if parent is not None:
            try:
                parent_category = Organization.objects.get(id=parent.id)

                if parent_category.max_subcategory_level <= parent_category.children.count():
                    raise serializers.ValidationError("Maximum subcategory level reached for the parent category.")
                validated_data['parent'] = parent_category  # Set the parent field
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Parent category does not exist.")
        else:
            parent_category = None
            validated_data['parent'] = parent_category
       
        return super().create(validated_data)
    
class OrgAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgAddress

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test


